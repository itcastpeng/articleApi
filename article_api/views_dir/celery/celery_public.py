from article_api import models
from article_api.publicFunc import Response, account
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, JsonResponse
from article_api.publicFunc.public import download_img, requests_video_download



# 下载资源
@csrf_exempt
@account.is_token(models.userprofile)
def download_inter(request, oper_type):
    response = Response.ResponseObj()
    if oper_type == 'img':
        pass

    elif oper_type == 'video':
        pass

    else:
        pass



    return JsonResponse(response.__dict__)













