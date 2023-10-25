import pycountry
from django.http import JsonResponse


def currencies(request):
    currencies_list = []
    for item in pycountry.currencies:
        currencies_list.append(item.alpha_3)

    return JsonResponse({'currencies': currencies_list})
