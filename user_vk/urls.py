from django.urls import path, include
from vk.views import main_page

urlpatterns = [
    path('', include('social_django.urls'), name='social'),
    path('', main_page, name='social_redirect'),
]

