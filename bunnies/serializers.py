from rest_framework import serializers

from bunnies.models import Bunny, RabbitHole


class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(many=True, queryset=Bunny.objects.all())
    bunny_count = serializers.SerializerMethodField()

    def get_bunny_count(self, obj):
        return Bunny.objects.filter(home=obj.id).count()

    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner')


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        bunnies = Bunny.objects.filter(home=obj.home.id).exclude(pk=obj.pk)
        return [bunny.name for bunny in bunnies]

    def validate(self, attrs):
        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')
