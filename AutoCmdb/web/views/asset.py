#!/usr/bin/env python
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from web.service import asset
class AssetListView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'asset_list.html')

class AssetJsonView(View):
    def get(self,request,*args,**kwargs):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self,request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self,request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

class AssetDetailView(View):
    def get(self,request, device_type_id, asset_nid):
        response = asser.Asset.assets_detail(device_type_id,asset_nid)
        return  render(request,'asset_list.html',{'response':response,'device_type_id':device_type_id})

class AddAssetView(View):
    def get(self,request,*args,**kwargs):
        return  render(request,'add_asset.html')