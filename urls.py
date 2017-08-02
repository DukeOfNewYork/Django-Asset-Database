from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_assets/$', views.add_assets, name='add_assets'),
    url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^all_assets/$', views.all_assets, name='list_locations'),
    url(r'^building/(\w+)/$', views.building_list, name='building_list'),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^export/$', views.export_moves, name='export'),
]
if settings.DEBUG:
    urlpatterns += [url(r'^media/(?P<path>.*)$', serve,
                        {'document_root': settings.MEDIA_ROOT,}),
                    ]
