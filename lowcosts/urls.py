"""lowcosts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from wizz import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    # url(r'^results', views.wizz, name='wizz'),
    url(r'^history', views.search_history, name='search-history'),
    url(r'^search', views.flight_search_form, name='search-form'),
    url(r'^requests', views.get_all_requests, name='all-requests'),
    url(r'^results/(?P<request_id>[\w{}.-]{1,12})/$', views.get_search_results, name='search-results'),
    url(r'^update/(?P<city_code>[\w{}.-]{1,3})/$', views.get_wizzair_airports, name='update-iata'),
]
