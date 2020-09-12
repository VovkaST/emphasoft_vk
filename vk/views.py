from django.shortcuts import render
from .functions import get_user_vk_friends


def main_page(request, *args, **kwargs):
    context = {
        'friends': get_user_vk_friends(user=request.user, k=5)
    }
    return render(request, 'vk_friends_list.html', context=context)


