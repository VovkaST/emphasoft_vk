from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from vk_api import vk_api, AuthError


class VKLogin(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        vk_app_id = request.META.get('VK_APP_ID')
        vk_app_secret_key = request.META.get('VK_APP_SECRET_KEY')
        vk_app_redirect_uri = request.META.get('VK_APP_REDIRECT_URI')
        vk_api_version = request.META.get('VK_API_VERSION')

        if code:
            context = {
                'vk': {
                    'code': code,
                    'VK_APP_ID': vk_app_id,
                    'VK_APP_SECRET_KEY': vk_app_secret_key,
                    'VK_APP_REDIRECT_URI': vk_app_redirect_uri,
                    'VK_API_VERSION': vk_api_version,
                },
            }

            try:
                vk_session = vk_api.VkApi(app_id=vk_app_id, client_secret=vk_app_secret_key, api_version=vk_api_version)
                vk_session.code_auth(code=code, redirect_url=vk_app_redirect_uri)
                api = vk_session.get_api()
                request.session['vk'] = {
                    'code': code,
                    'token': vk_session.token,
                }
                # return HttpResponseRedirect('/')
            except AuthError as exc:
                context['error'] = exc.args[0]

        return render(request, 'user_vk/login.html', context=context)
