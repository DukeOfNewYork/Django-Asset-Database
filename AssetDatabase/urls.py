from django.conf.urls import url

from django.conf import settings
from django.views.static import serve
from . import views

app_name = 'AssetDatabase'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^administration/$', views.administration, name='administration'),
    url(r'^building/(\w+)/$', views.building_list, name='building_list'),
    url(r'^all_assets/$', views.all_assets, name='list_locations'),
    url(r'^all_weeks/$', views.all_weeks, name='all_weeks'),
    url(r'^all_weeks/([-\w]+)/$', views.week_of_list, name='week_of_list'),
    url(r'^export_week/([-\w]+)/$', views.export_week, name='export_weeks'),
    url(r'^export/$', views.export_moves, name='export'),
    url(r'^image_upload/$', views.image_upload, name='upload'),
    url(r'^image_scan/$', views.image_scan, name='scan'),
    url(r'^add_assets/$', views.add_assets, name='add_assets'),
    url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^add_building/$', views.add_building, name='add_building'),
    url(r'^remove_building/$', views.remove_building, name='remove_building'),
    url(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]

urlpatterns += [url(r'^media/(?P<path>.*)$', serve,
                        {'document_root': settings.MEDIA_ROOT,}),
                    ]
