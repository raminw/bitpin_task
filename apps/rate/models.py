from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.common.model_mixins import TimeMixin
from apps.rate.managers import RateManager
from apps.user.models import User
from apps.post.models import Post


class Rate(TimeMixin, models.Model):
    objects = RateManager()

    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='rated_post')
    rater = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rater_user')
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])
    is_effective = models.BooleanField(default=True)

    def __str__(self):
        return self.rater.username

    class Meta:
        ordering = ['id']
        db_table = 'rate'
        unique_together = ('post', 'rater',)
