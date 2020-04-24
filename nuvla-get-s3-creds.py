#!/usr/bin/env python3

import logging
import requests
import os
import time
import sys

from nuvla.api import Api as Nuvla, NuvlaError

RETRY_EXCEPTIONS = (requests.exceptions.ConnectTimeout, NuvlaError, requests.exceptions.HTTPError)

log = None
log_levels_map = {'info': logging.INFO,
                  'debug': logging.DEBUG,
                  'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'fatal': logging.FATAL,
                  'warn': logging.WARN}


def log_init(config):
    global log

    module_name = os.path.basename(sys.argv[0]).replace('.py', '')

    log_level = log_levels_map.get(
        config.get('logging', {}).get('level', 'info').lower())
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s')

    log = logging.getLogger(module_name)
    log.setLevel(log_level)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(log_formatter)
    log.addHandler(stdout_handler)

    if config.get('logging', {}).get('file', False):
        log_file = '{0}.log.{1}'.format(module_name, int(time.time()))
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(log_formatter)
        log.addHandler(file_handler)


def nuvla_init(config):
    log.info("Authenticating with Nuvla...")
    nuvla_endpoint = os.environ.get('NUVLA_ENDPOINT') or config['nuvla'].get('endpoint')
    nuvla = Nuvla(endpoint=nuvla_endpoint)

    n = 0
    ts = time.time()

    while True:
        try:
            if 'NUVLA_API_KEY' in os.environ and 'NUVLA_API_SECRET' in os.environ:
                nuvla.login_apikey(
                    os.environ['NUVLA_API_KEY'], os.environ['NUVLA_API_SECRET'])
            else:
                nuvla.login_password(
                    config['nuvla']['key'], config['nuvla']['secret'])
            break
        except RETRY_EXCEPTIONS as ex:
            log.error("Authenticating with Nuvla... failed: {}".format(ex))
            st = 2**n
            log.info("Authenticating with Nuvla... re-attempting in {} sec."
                     .format(st))
            time.sleep(st)
            n = (n < 7) and (n + 1) or 0
    log.info("Authenticating with Nuvla... done. (time took: {} sec)"
             .format(int(time.time() - ts)))
    return nuvla


def find_s3_creds(nuvla):
    depl_id = os.environ.get('NUVLA_DEPLOYMENT_ID')

    # Go up from deployment to infra service (IS) group:
    # deployment -> IS creds -> IS -> IS group
    # Find S3 IS in the group and find IS creds of it:
    # IS group -> S3 IS -> S3 IS creds

    # Deployment
    res = nuvla.get(depl_id)

    # IS creds is the parent of the deployment.
    infra_service_cred_id = res.data['parent']
    res = nuvla.get(infra_service_cred_id)

    # IS is the parent of the IS creds.
    infra_service_id = res.data['parent']
    res = nuvla.get(infra_service_id)

    # IS group is the parent of IS.
    infra_service_group = res.data['parent']
    res = nuvla.get(infra_service_group)

    # Find S3 IS in the group.
    s3_infra_service = None
    for infra_service in map(lambda x: x['href'], res.data['infrastructure-services']):
        res = nuvla.get(infra_service)
        if 's3' == res.data['subtype']:
            s3_infra_service = res.data
            break

    # Get all creds who's parent is S3 IS.
    s3_infra_service_id = s3_infra_service['id']
    _filter = "parent='{}'".format(s3_infra_service_id)
    res = nuvla.search('credential', filter=_filter)
    if res.count < 1:
        raise SystemExit('No creds fround for IS {}'.format(s3_infra_service_id))
    # Grab the first one and extract the creds.
    s3_infra_service_creds = res.data['resources'][0]
    key = s3_infra_service_creds['access-key']
    secret = s3_infra_service_creds['secret-key']
    endpoint = s3_infra_service['endpoint']

    return endpoint, key, secret


def main():
    nuvla = nuvla_init({})
    # print(dir(nuvla.)
    endpoint, key, secret = find_s3_creds(nuvla)
    log.info('endpoint: %s' % endpoint)
    log.info('key: %s' % key)
    log.info('secret: %s' % secret)


if __name__ == "__main__":
    log_init({})
    main()