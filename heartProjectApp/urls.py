# yourappname/urls.py
from django.urls import path
from .views import choropleth_map, display_images,home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', home, name='home'),
    path('display_images/<str:category>/', display_images, name='display_images'),
    path('choropleth/', choropleth_map, name='choropleth_map'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
