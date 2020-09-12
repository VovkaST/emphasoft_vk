from django.urls import path, include
from vk.views import main_page

urlpatterns = [
    path('login_vk/', include('social_django.urls'), name='social'),
    path('login_vk/', main_page, name='social_redirect'),
]

