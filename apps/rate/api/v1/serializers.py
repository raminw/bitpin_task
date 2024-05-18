from rest_framework import serializers

from apps.rate.models import Rate


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        read_only_fields = ('id', 'rater', 'created_at', 'updated_at')
        exclude = ('is_effective',)
