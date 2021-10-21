from typing import Optional
from django.forms.models import model_to_dict
from rest_framework.decorators import action
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models.unique_searchfilter import UniqueKeyword, UniqueLocationDisplayname
from .models.videoitem import Videoitem
from .models.videoitems_list import VideoitemsList
from .paginations import VideoitemsPagination
from .filters import LocationFilter, VideoitemsFilter
from .serializers import (
    TypingHintsSerializer,
    UniqueSearchfiltersSerializer,
    VideoitemsListSerializer,
    VideoitemsSerializer,
    VideoitemEntrySerializer,
)

DEFAULT_ERRORS = {"auth": {"error": "Not authenticated"}}


class VideoitemView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    model = Videoitem
    queryset = Videoitem.objects.all()
    serializer_class = VideoitemsSerializer
    pagination_class = VideoitemsPagination

    def get_queryset(self, *args, **kwargs):
        orderby = self.request.GET.get("orderby") or "-exif_last_modified"
        qs = super().get_queryset().order_by(orderby)
        data = VideoitemsFilter(self.request.GET, queryset=qs)

        return data.qs


class VideoitemEntryView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = VideoitemEntrySerializer
    queryset = Videoitem.objects.all()

    def get_queryset(self, *args, **kwargs):
        return [Videoitem.objects.get(pk=self.request.query_params["pk"])]


class KeywordHintsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TypingHintsSerializer
    queryset = UniqueKeyword.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(keyword__startswith=self.request.GET.get("s"))[:10]


class LocationHintsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TypingHintsSerializer
    queryset = UniqueLocationDisplayname.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        data = LocationFilter(self.request.GET, queryset=qs)
        return data.qs


class InitSearchfilterDropdowns(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Gets initial values for frontend dropdown menus."""

    permission_classes = (AllowAny,)
    serializer_class = UniqueSearchfiltersSerializer

    def get_queryset(self):
        q = {"response": ...}
        return q


class VideoitemsListView(viewsets.ModelViewSet):
    # work in progress
    """Views and methods for handling user lists."""

    permission_classes = (IsAuthenticated,)
    serializer_class = VideoitemsListSerializer
    queryset = VideoitemsList.objects.all()

    def user_is_authenticated(self) -> bool:
        try:
            return self.request.user.is_authenticated
        except AttributeError:
            return False

    def get_instance_if_permitted(self) -> Optional[VideoitemsList]:
        try:
            user = self.request.user
            if user.is_authenticated:
                instance = self.get_object()
                if instance.created_by == user:
                    return instance
        except AttributeError:
            return None

    def get_user(self):
        if self.user_is_authenticated():
            return self.request.user
        return None

    def serialize_instance(self, instance):
        model_dict = model_to_dict(instance)
        response = {
            **model_dict,
            "videoitems": [
                {"pk": obj.pk, "thumbnail_count": obj.static_thumbnail_count}
                for obj in model_dict["videoitems"]
            ],
        }
        return response

    @action(detail=True, methods=["post"], url_path="add_to_list")
    def add_to_list(self, request, *args, **kwargs):
        """Add one or more videoitem(s) to a user list"""
        instance = self.get_instance_if_permitted()
        if not instance:
            return Response(DEFAULT_ERRORS["auth"], status=status.HTTP_200_OK)

        if "videoitems" in request.data:
            # legg inn kontroll av bruker opp mot permissions for videoitems.
            instance.videoitems.add(
                *Videoitem.objects.filter(pk__in=request.data["videoitems"])
            )

        return Response(self.serialize_instance(instance), status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="remove_from_list")
    def remove_from_list(self, request, *args, **kwargs):
        """Remove one or more videoitem(s) from a user list"""
        # instance = self.get_object()
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="new_list")
    def new_list(self, request, *args, **kwargs):
        """Create new videoitems user list"""
        try:
            if not (
                self.user_is_authenticated()
                or request.data["user_id"] != request.user.id
            ):
                return Response(DEFAULT_ERRORS["auth"], status=status.HTTP_200_OK)

            if not request.data["list_label"]:
                return Response({"error": "Missing label"}, status=status.HTTP_200_OK)

        except AttributeError:
            return Response(DEFAULT_ERRORS["auth"], status=status.HTTP_200_OK)

        user = self.request.user
        label = request.data["list_label"]

        if user.videoitems_lists.filter(label=label):
            return Response({"error": "Duplicate label"}, status=status.HTTP_200_OK)

        new_obj = VideoitemsList.objects.create(label=label, created_by=user)

        if request.data["videoitems"]:
            # må begrenses til bare brukerens egne filer.
            new_obj.videoitems.add(
                *Videoitem.objects.filter(pk__in=request.data["videoitems"])
            )

        user.videoitems_lists.add(new_obj)

        return Response(self.serialize_instance(new_obj), status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="edit_list_name")
    def edit_list_name(self, request, *args, **kwargs):
        # instance = self.get_object()
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="delete_list")
    def delete_list(self, request, *args, **kwargs):
        # instance = self.get_object()
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="get_user_lists")
    def get_user_lists(self, request, *args, **kwargs):
        """Get all of user's lists"""
        user = self.get_user()
        if not user:
            return Response(DEFAULT_ERRORS["auth"], status=status.HTTP_200_OK)
        return Response(
            VideoitemsListSerializer(
                VideoitemsList.objects.filter(user=user), many=True
            ).data
        )

    @action(detail=True, methods=["get"], url_path="get_user_list")
    def get_user_list(self, request, *args, **kwargs):
        """Get single user list"""
        instance = self.get_object()
        model_dict = model_to_dict(instance)
        response = {
            **model_dict,
            "videoitems": [str(obj) for obj in model_dict["videoitems"]],
        }
        return Response(response, status=status.HTTP_200_OK)
