#!/usr/bin/env python
import os
import json
import time
import hashlib
import requests
from src import plugins
from config import settings
from lib.serialize import Json
from lib.log import Logger
from concurrent.futures import ThreadPoolExecutor

class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API
        self.key = settings.KEY
        self.key_name = settings.AUTH_KEY_NAME

    def auth_key(self):
        ha = hashlib.md5(self.key.encode('utf-8'))
        time_span = time.time()
        ha.update(bytes("%s|%f")%(self.key,time_span),encoding='utf-8')
        encryption = ha.hexdigest()
        result = "%s|%f"% (encryption,time_span)
        return {self.key_name:result}

    def get_asset(self):
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.get(
                url=self.asset_api,
                headers=headers
            )
        except Exception as e:
            response = e
        return response.json()

    def post_asset(self,msg,callback=None):
        status = True
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.post(
                url=self.asset_api,
                headers=headers,
                json=msg
            )
        except Exception as e:
            response = e
            status = False
        if callback:
            callback(status, response)

    def process(self):
        raise NotImplementedError('you must implement process method')

    def callback(self, status, response):
        if not status:
            Logger().log(str(response),False)
        ret = json.loads(response.text)
        if ret['code'] ==10000:
            Logger().log(ret['message'],True)
        else:
            Logger().log(ret['message'],False)

class AutoAgent(AutoBase):
    def __init__(self):
        self.cert_file_path = settings.CERT_FILE_PATH
        super(AutoAgent,self).__init__()

    def load_local_cert(self):
        if not os.path.exists(self.cert_file_path):
            return None
        with open(self.cert_file_path,mode='r') as f:
            data = f.read()
        if not data:
            return None
        cert = data.strip()
        return cert

    def write_local_cert(self,cert):
        if not os.path.exists(self.cert_file_path):
            os.makedirs(os.path.dirname(self.cert_file_path))
        with open(settings.CERT_FILE_PATH,mode='w') as f:
            f.write(cert)

    def process(self):
        server_info = plugins.get_server_info()
        if not server_info.status:
            return
        local_cert = self.load_local_cert()
        if not local_cert:
            if local_cert == server_info.data['hostname']:
                pass
            else:
                server_info.data['hostname'] = local_cert
        else:
            self.write_local_cert(server_info.data['hostname'])
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json,self.callback)

class AutoSSH(AutoBase):
    def process(self):
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'],False)
        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run,hostname)
        pool.shutdown(wait=True)

    def run(self,hostname):
        server_info = plugins.get_server_info(hostname)
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json,self.callback)

class AutoSalt(AutoBase):
    def process(self):
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'],False)

        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run,hostname)
        pool.shutdown(wait=True)

    def run(self,hostname):
        server_info = plugins.get_server_info(hostname)
        # 序列化成字符串
        server_json = Json.dumps(server_info.data)
        # 发送到API
        self.post_asset(server_json, self.callback)