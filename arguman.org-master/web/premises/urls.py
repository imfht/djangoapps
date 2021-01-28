from django.conf.urls import patterns, url
from premises.views import (ContentionDetailView, HomeView,
                            ArgumentCreationView, PremiseCreationView,
                            PremiseDeleteView, ContentionJsonView,
                            PremiseEditView, ArgumentUpdateView,
                            ArgumentPublishView, ArgumentUnpublishView,
                            ArgumentDeleteView, AboutView, NewsView,
                            UpdatedArgumentsView, ReportView, RemoveReportView,
                            ControversialArgumentsView, TosView, SearchView,
                            NotificationsView, PremiseSupportView, PremiseUnsupportView,
                            StatsView, FallaciesView, FeaturedJSONView, NewsJSONView,
                            RandomArgumentView)


urlpatterns = patterns('',
   url(r'^$', HomeView.as_view(), name='home'),
   url(r'^notifications$', NotificationsView.as_view(), name='notifications'),
   url(r'^featured.json$', FeaturedJSONView.as_view(), name='contentions_featured_json'),
   url(r'^news.json$', NewsJSONView.as_view(), name='contentions_latest_json'),
   url(r'^news$', NewsView.as_view(),
       name='contentions_latest'),
   url(r'^search$', SearchView.as_view(),
       name='contentions_search'),
   url(r'^random$', RandomArgumentView.as_view(),
       name='contentions_random'),
   url(r'^updated$', UpdatedArgumentsView.as_view(),
       name='contentions_updated'),
   url(r'^controversial', ControversialArgumentsView.as_view(),
       name='contentions_controversial'),
   url(r'^stats$', StatsView.as_view(),
       name='contentions_stats'),
    url(r'^fallacies$', FallaciesView.as_view(),
       name='fallacies'),
   url(r'^about$',
       AboutView.as_view(),
       name='about'),
   url(r'^tos$',
       TosView.as_view(),
       name='tos'),
   url(r'^new-argument$',
       ArgumentCreationView.as_view(),
       name='new_argument'),
   url(r'^(?P<slug>[\w-]+)/edit$',
        ArgumentUpdateView.as_view(),
        name='contention_edit'),
   url(r'^(?P<slug>[\w-]+)\.json$',
        ContentionJsonView.as_view(),
        name='contention_detail_json'),
   url(r'^(?P<slug>[\w-]+)$',
        ContentionDetailView.as_view(),
        name='contention_detail'),
   url(r'^(?P<slug>[\w-]+)/(?P<premise_id>[\d+]+)$',
        ContentionDetailView.as_view(),
        name='premise_detail'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/unsupport',
        PremiseUnsupportView.as_view(),
        name='unsupport_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/support',
        PremiseSupportView.as_view(),
        name='support_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/delete',
        PremiseDeleteView.as_view(),
        name='delete_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/report',
        ReportView.as_view(),
        name='report_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/unreport',
        RemoveReportView.as_view(),
        name='unreport_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/new',
        PremiseCreationView.as_view(),
        name='insert_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)',
        PremiseEditView.as_view(),
        name='edit_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/new',
        PremiseCreationView.as_view(),
        name='new_premise'),
    url(r'^(?P<slug>[\w-]+)/publish',
        ArgumentPublishView.as_view(),
        name='contention_publish'),
    url(r'^(?P<slug>[\w-]+)/unpublish',
        ArgumentUnpublishView.as_view(),
        name='contention_unpublish'),
    url(r'^(?P<slug>[\w-]+)/delete',
        ArgumentDeleteView.as_view(),
        name='contention_delete'),
)