from rest_framework import serializers
from django.conf import settings

from apps.post.models import Post
from apps.rate.models import Rate
from apps.rate.api.v1.serializers import RateSerializer
from apps.user.api.v1.serializers import UserMinimalSerializer
from apps.common.utils import safe_get_user_from_context


class PostSerializer(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    my_rate = serializers.SerializerMethodField()

    def get_average_rate(self, post: Post):
        return round(post.average_rate, settings.ROUNDING_AVERAGE_RATE_DIGIT_COUNT)

    def get_writer(self, post: Post):
        return UserMinimalSerializer(post.writer).data

    def get_my_rate(self, post: Post):
        try:
            user = safe_get_user_from_context(self.context)
            if user.id:
                return RateSerializer(Rate.objects.get_user_post_rate(user.id, post.id)).data
        except Rate.DoesNotExist:
            return

    class Meta:
        model = Post
        read_only_fields = (
            'id', 'rate_count', 'average_rate', 'total_rate', 'created_at', 'updated_at', 'writer', 'my_rate'
        )
        exclude = ('is_active', 'last_rate_time',)

    def create(self, validated_data):
        return Post.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
            writer=safe_get_user_from_context(self.context)
        )
