from django.db import models


class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).get_queryset().filter(is_active=True)

    def get_active_by_id(self, post_id: int):
        return self.active().get(id=post_id)
