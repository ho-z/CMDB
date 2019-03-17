#!/usr/bin/env python

from django.views import View

class LoginView(View):
    def get(self,request,*args,**kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        pass