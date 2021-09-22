from rest_framework import viewsets, mixins
from .paginations import VideoitemsPagination
from .models.unique_searchfilter import UniqueKeyword, UniqueLocationDisplayname
from .models.videoitem import Videoitem
from .filters import LocationFilter, VideoitemsFilter
from .serializers import (
    TypingHintsSerializer,
    UniqueSearchfiltersSerializer,
    VideoitemsSerializer,
    VideoitemEntrySerializer,
)

class VideoitemView(mixins.ListModelMixin, viewsets.GenericViewSet):
    model = Videoitem
    queryset = Videoitem.objects.all()
    serializer_class = VideoitemsSerializer
    pagination_class = VideoitemsPagination

    def get_queryset(self, *args, **kwargs):
        orderby = self.request.GET.get('orderby') or '-exif_last_modified'
        qs = super().get_queryset().order_by(orderby)
        data = VideoitemsFilter(self.request.GET, queryset=qs)

        return data.qs


class VideoitemEntryView(viewsets.ModelViewSet):
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
    serializer_class = UniqueSearchfiltersSerializer
    def get_queryset(self):
        q = { 'response': ... }
        return q