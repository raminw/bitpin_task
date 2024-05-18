from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.common.model_mixins import TimeMixin
from apps.user.models import User
from apps.post.managers import PostManager


class Post(TimeMixin, models.Model):
    objects = PostManager()

    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='writer_user')
    title = models.CharField()
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    rate_count = models.PositiveIntegerField(default=0)
    total_rate = models.PositiveIntegerField(default=0)
    average_rate = models.FloatField(validators=[MaxValueValidator(5), MinValueValidator(0)],
                                     null=True)
    last_rate_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        db_table = 'post'
