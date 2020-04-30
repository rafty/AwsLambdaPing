# -*- coding: utf-8 -*-
import os
import socket
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

RETRY = 3
HOST = os.getenv('TEST_SERVER_DNS_NAME')
PORT = int(os.getenv('TEST_SERVER_PORT_NO'))


def ping(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        logger.info('connected')
        sock.close()
        return True
    except socket.error as e:
        if 'Connection refused' in e.args:
            logger.info('Connection refused')
            return True
        if 'timed out' in e.args:
            logger.info('timed out')
            raise e


def lambda_handler(event, context):
    count = 0
    for _ in range(RETRY):
        try:
            count += 1
            if ping(HOST, PORT):
                logger.info('Server is alive!')
                break
        except Exception as e:
            if 'timed out' in e.args:
                logger.info('Server is down!')
                if count >= RETRY:
                    logger.error(f'Server({HOST}) is Down!')
            else:
                logger.error(e)
