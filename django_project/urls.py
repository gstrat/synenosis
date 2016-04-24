from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from synenosis.api import router


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^', include('demoapp.urls')),
)



if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
