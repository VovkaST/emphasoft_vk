from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .functions import get_user_vk_friends


@login_required
def main_page_view(request, *args, **kwargs):
    context = {
        'friends': get_user_vk_friends(user=request.user, k=5)
    }
    return render(request, 'vk_friends_list.html', context=context)


