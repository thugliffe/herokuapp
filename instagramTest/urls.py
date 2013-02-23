from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from instagramTest import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instagramTest.views.home', name='home'),
    # url(r'^instagramTest/', include('instagramTest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'instagramTest.instagram.views.login_user',name='loginpage'),
     (r'^instagram/auth/$', 'instagramTest.instagram.views.validateUser'),
     # url(r'^instagram/auth/$', RedirectView.as_view(url='/instagram/'), name='instagram'),
     url(r'^instagram/(?P<userID>\d+)/$', 'instagramTest.instagram.views.instagram',name="userPage"),
     url(r'^instagram/(?P<userID>\d+)/(?P<maxId>\S+)/$', 'instagramTest.instagram.views.instagramNext',name="userImagePages"),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
