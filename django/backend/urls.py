#from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from videodb import views

router = routers.DefaultRouter()

router.register(r'videoitems', views.VideoitemView, 'videoitems')

router.register(r'entry/videoitem', views.VideoitemEntryView, 'videoitem')

router.register(r'init/searchfilter_dropdowns', views.InitSearchfilterDropdowns, 'init_searchfilter_dropdowns')

router.register(r'typinghints/keyword', views.KeywordHintsView, 'keywordhints')
router.register(r'typinghints/location', views.LocationHintsView, 'locationhints')

urlpatterns = [
    path('api/', include(router.urls))
] 