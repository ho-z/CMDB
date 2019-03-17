#!/usr/bin/env python
#coding=utf-8
__author__ = 'Zhangliang'

from src.client import AutoAgent
from src.client import AutoSalt
from src.client import AutoSSH
from config import settings

def client():
    if settings.MODE == 'agent':
        cli = AutoAgent()
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置正确的资产采集信息方式，如：agent、ssh、salt')
    cli.process()