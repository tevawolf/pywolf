from django.shortcuts import render


def create_village(request):

    # マスタから値を取得する

    context = {}

    return render(request, 'pywolf/create_village.html', context)
