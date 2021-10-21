# from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from videodb import views

router = routers.DefaultRouter()

router.register(r"videoitems", views.VideoitemView, "videoitems")
router.register(r"entry/videoitem", views.VideoitemEntryView, "videoitem")
router.register(
    r"init/searchfilter_dropdowns",
    views.InitSearchfilterDropdowns,
    "init_searchfilter_dropdowns",
)
router.register(r"typinghints/keyword", views.KeywordHintsView, "keywordhints")
router.register(r"typinghints/location", views.LocationHintsView, "locationhints")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(("core.routers", "core"), namespace="core-api")),
    path(
        "api/<int:user_id>/lists/",
        views.VideoitemsListView.as_view({"get": "get_user_lists"}),
        name="get all of user lists",
    ),
    path(
        "api/<int:user_id>/lists/<int:pk>/",
        views.VideoitemsListView.as_view({"get": "get_user_list"}),
        name="get single userlist",
    ),
    path(
        "api/<int:user_id>/lists/<int:pk>/add/",
        views.VideoitemsListView.as_view({"post": "add_to_list"}),
        name="add videoitem(s) to userlist",
    ),
    path(
        "api/<int:user_id>/lists/<int:pk>/remove/",
        views.VideoitemsListView.as_view({"delete": "remove_from_list"}),
        name="remove videoitem(s) from userlist",
    ),
    path(
        "api/<int:user_id>/lists/new/<str:list_label>/",
        views.VideoitemsListView.as_view({"post": "new_list"}),
        name="new userlist",
    ),
]
