#!/usr/bin/env python
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse

class CpuPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from config.settings import BASEDIR
                output = open(os.path.join(BASEDIR,'files/cpuinfo.out'),'r').read()
            else:
                shell_command = "cat /proc/cpuinfo"
                output = self.exec_shell_cmd(shell_command)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux cpu plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    @staticmethod
    def parse(content):
        response = {'cpu_count':0,'cpu_physical_count':0,'cpu_mode1':''}

        cpu_physical_set = set()
        content = content.strip()
        for item in content.split('\n\n'):
            for row_line in item.split('\n'):
                key,value = row_line.split(':')
                key = key.strip()
                if key == 'processer':
                    response['cpu_count'] += 1
                elif key == 'physical id':
                    cpu_physical_set.add(value)
                elif key == 'model name':
                    if not response['cpu_mode1']:
                        response['cpu_mode1'] = value
        response['cpu_physical_count'] = len(cpu_physical_set)

        return response