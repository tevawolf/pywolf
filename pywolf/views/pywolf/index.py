from django.shortcuts import render

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import PLAccount


def index(request):
    """トップページ表示"""
    pl_list = PLAccount.objects.order_by('id')
    village_list = Village.objects.order_by('village_no')
    context = {'village_list': village_list, 'pl_list': pl_list}
    return render(request, 'pywolf/index.html', context)