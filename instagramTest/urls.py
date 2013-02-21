from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

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
     (r'^$', 'instagramTest.instagram.views.login_user'),
     (r'^instagram/auth/$', 'instagramTest.instagram.views.validateUser'),
     # url(r'^instagram/auth/$', RedirectView.as_view(url='/instagram/'), name='instagram'),
     url(r'^instagram/(?P<userID>\d+)/$', 'instagramTest.instagram.views.instagram',name="userPage"),
)
