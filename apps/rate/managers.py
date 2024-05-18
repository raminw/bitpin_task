from bulk_update_or_create import BulkUpdateOrCreateMixin

from django.db import models
from django.db.models import Sum


class RateManager(models.Manager, BulkUpdateOrCreateMixin):
    def active(self):
        return super(RateManager, self).get_queryset().filter(is_effective=True)

    def get_user_post_rate(self, user_id: int, post_id: int):
        return self.active().get(rater=user_id, post_id=post_id)

    def get_sum_and_count(self, post_id: int) -> [int, int]:
        post_rates = self.active().filter(post_id=post_id)
        rate_count = post_rates.count()
        sum_rate_score = post_rates.aggregate(Sum('score'))
        return sum_rate_score['score__sum'], rate_count
