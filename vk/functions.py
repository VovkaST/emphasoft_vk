import random

from social_core.backends.vk import VKOAuth2
from social_django.models import UserSocialAuth
from vk_api import VkApi


def get_access_token(user, provider) -> str:
    """
    Возвращает ключ доступа заданного пользователя и провайдера.
    В случае отсутствия возвращает None.
    :param user: Экземпляр класса пользователя Django.
    :param str provider: Строка имени провайдера SocialAuth.
    """
    try:
        if hasattr(user, 'social_user'):
            social_user = user.social_user
        else:
            social_user = UserSocialAuth.objects.get(user=user.id, provider=provider)
    except UserSocialAuth.DoesNotExist:
        return None

    return social_user.extra_data.get('access_token')


def get_user_vk_friends(user, k=3) -> list:
    """
    Возвращает k случайных друзей ВКонтакте заданного пользователя.

    :param user: Экземпляр класса пользователя Django.
    :param int k: Длина возвращаемого списка.
    """
    friends = []
    token = get_access_token(user=user, provider=VKOAuth2.name)
    if token:
        vk_session = VkApi(token=token)
        api = vk_session.get_api()
        friends_list = api.friends.get(fields='domain,city,country,photo_100')
        for item in random.sample(population=friends_list.get('items'), k=k):
            city = item.get('city', dict()).get('title', '')
            country = item.get('country', dict()).get('title', '')
            friends.append({
                'network_status': 'В сети' if item.get('online') else 'Не в сети',
                'vk_link': 'https://vk.com/{}'.format(item.get('domain')),
                'name': '{} {}'.format(item.get('last_name'), item.get('first_name')),
                'avatar': item.get('photo_100'),
                'city': ', '.join((city, country)) if all((city, country)) else f'{city}{country}'
            })
    return friends
