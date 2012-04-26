from django.conf.urls.defaults import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    (r'^$', 'bedroom.views.home'),
    (r'^submit$', 'bedroom.views.submit'),
    (r'^about$', 'bedroom.views.about'),
    (r'^submit/picture$', 'bedroom.views.upload_picture'),
    (r'^submit/bedroom$', 'bedroom.views.submit_bedroom'),

#    url(r'^help/$', direct_to_template, {'template': 'help.html'}),
#
#    url(r'^edit/?$', 'interface.views.editTeam', name='editTeam'),
#    url(r'^remove/?(?P<id>[a-z\d]+)/$', 'interface.views.removePlayer'),
#    url(r'^add/?(?P<id>[a-z\d]+)/$', 'interface.views.addPlayer'),
#
#    (r'^accounts/profile/.*', 'interface.views.home'),
#    (r'^users/.*', 'interface.views.home'),
#    (r'^accounts/', include('registration.urls')),
#
#    # Uncomment the admin/doc line below to enable admin documentation:
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
)
