from article_api import models
from article_api.publicFunc import Response, account
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, JsonResponse
from article_api.publicFunc.public import get_content



# 定时更新文章
# @csrf_exempt
# @account.is_token(models.userprofile)
def celery_regularly_update_articles(request):
    response = Response.ResponseObj()
    objs = models.article.objects.filter(original_link__isnull=False)
    for obj in objs:
        original_link = obj.original_link
        data = get_content(original_link, get_content=1)
        obj.content = data.get('content')
        obj.save()


    return JsonResponse(response.__dict__)













