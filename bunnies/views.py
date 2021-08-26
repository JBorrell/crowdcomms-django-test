from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponseBadRequest

from bunnies.models import Bunny, RabbitHole
from bunnies.permissions import RabbitHolePermissions
from bunnies.serializers import BunnySerializer, RabbitHoleSerializer


class RabbitHoleViewSet(viewsets.ModelViewSet):
    serializer_class = RabbitHoleSerializer
    permission_classes = (IsAuthenticated, RabbitHolePermissions)
    queryset = RabbitHole.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


class BunnyViewSet(viewsets.ModelViewSet):
    serializer_class = BunnySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bunny.objects.all()

    def create(self, request, *args, **kwargs):
        rabbit_hole = RabbitHole.objects.get(location=request.data.get('home'))
        if rabbit_hole.bunnies.count() >= rabbit_hole.bunnies_limit:
            return HttpResponseBadRequest()
        else:
            return super().create(request, *args, **kwargs)
