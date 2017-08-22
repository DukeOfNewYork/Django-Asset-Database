from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^building/(\w+)/$', views.building_list, name='building_list'),
    url(r'^all_assets/$', views.all_assets, name='list_locations'),
    url(r'^all_weeks/$', views.all_weeks, name='all_weeks'),
    url(r'^all_weeks/([-\w]+)/$', views.week_of_list, name='week_of_list'),
    url(r'^export_week/([-\w]+)/$', views.export_week, name='export_weeks'),
    url(r'^search-form/$', views.search_form),
    url(r'^export/$', views.export_moves, name='export'),
    url(r'^add_assets/$', views.add_assets, name='add_assets'),
]

urlpatterns += [url(r'^media/(?P<path>.*)$', serve,
                        {'document_root': settings.MEDIA_ROOT,}),
                    ]
