# from core.serializers import UserSerializer
from django.db.models import query
from django.http import response
from rest_framework import viewsets, mixins, serializers, generics
from rest_framework.views import APIView
from .paginations import VideoitemsPagination
from .models.unique_searchfilter import UniqueKeyword, UniqueLocationDisplayname
from .models.videoitem import Videoitem
from .filters import LocationFilter, VideoitemsFilter
from .serializers import (
    TypingHintsSerializer,
    UniqueSearchfiltersSerializer,
    VideoitemsListSerializer,
    VideoitemsSerializer,
    VideoitemEntrySerializer,
)
from .models.videoitems_list import VideoitemsList
from django.forms.models import model_to_dict
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class VideoitemView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    model = Videoitem
    queryset = Videoitem.objects.all()
    serializer_class = VideoitemsSerializer
    pagination_class = VideoitemsPagination

    def get_queryset(self, *args, **kwargs):
        # print(self.request.headers)
        # print(args)
        # print(kwargs)
        orderby = self.request.GET.get('orderby') or '-exif_last_modified'
        qs = super().get_queryset().order_by(orderby)
        data = VideoitemsFilter(self.request.GET, queryset=qs)

        return data.qs


class VideoitemEntryView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = VideoitemEntrySerializer
    queryset = Videoitem.objects.all()

    def get_queryset(self, *args, **kwargs):
        q = [Videoitem.objects.get(videoitem_id=str(self.request.query_params.get('pk')))]
        return q

class KeywordHintsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TypingHintsSerializer
    queryset = UniqueKeyword.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(keyword__startswith=self.request.GET.get('s'))[:10]


class LocationHintsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TypingHintsSerializer
    queryset = UniqueLocationDisplayname.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        data = LocationFilter(self.request.GET, queryset=qs)
        return data.qs


class InitSearchfilterDropdowns(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UniqueSearchfiltersSerializer
    def get_queryset(self):
        q = { 'response': ... }
        return q

        
class VideoitemsListView(viewsets.ModelViewSet):
    # in early development
    permission_classes = [AllowAny]
    serializer_class = VideoitemsListSerializer
    queryset = VideoitemsList.objects.all()

    @action(detail=True, methods=['post'], url_path='add_to_list')
    def add_to_list(self, request, *args, **kwargs):
        print('test',request.user)
        instance = self.get_object()
        if 'videoitems' in request.data:
            instance.videoitems.add(*Videoitem.objects.filter(pk__in=request.data['videoitems']))
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='remove_from_list')
    def remove_from_list(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance',instance)
        print('kwargs', kwargs)
        print('request.data',request.data)
        custom_response = {"test": "hello world"}

        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='new_list')
    def new_list(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance',instance)
        print('kwargs', kwargs)
        print('request.data',request.data)
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='edit_list_name')
    def edit_list_name(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance',instance)
        print('kwargs', kwargs)
        print('request.data',request.data)
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='delete_list')
    def delete_list(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance',instance)
        print('kwargs', kwargs)
        print('request.data',request.data)
        custom_response = {"test": "hello world"}
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='get_user_lists')
    def get_user_lists(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        print('test',request)
        qs = VideoitemsList.objects.filter(user_id=user_id)
        return Response(VideoitemsListView(qs, many=True).data)

    @action(detail=True, methods=['get'], url_path='get_user_list')
    def get_user_list(self, request, *args, **kwargs):
        instance = self.get_object()
        model_dict = model_to_dict(instance)
        print('test',request)
        response = {
            **model_dict,
            'videoitems': [str(obj) for obj in model_dict["videoitems"]]
        }
        return Response(response, status=status.HTTP_200_OK)



