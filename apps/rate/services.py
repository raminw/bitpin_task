import logging
import json
from datetime import datetime
from redis import Redis
from concurrent.futures import ThreadPoolExecutor


from apps.post.models import Post
from apps.rate.models import Rate
from apps.rate.dtos import RateRedisObjectDTO

from django.conf import settings


class RateService:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.redis = Redis(connection_pool=settings.REDIS_CONNECTION_POOL)

    def add_rate_to_redis(self, rate_dto: RateRedisObjectDTO):
        try:
            posts_rates_dict = self.get_rate_obj_redis()
            post_id = str(rate_dto.post_id)
            if not posts_rates_dict.get(post_id):
                posts_rates_dict[post_id] = list()
            posts_rates_dict[post_id].append(rate_dto.to_dict())
            self.set_rate_obj_redis(posts_rates_dict)
        except Exception as e:
            self.logger.error(f"function:[add_rate_to_redis] error:[{e}]")

    def get_rate_obj_redis(self) -> dict:
        try:
            post_rates_dict = self.redis.get(settings.REDIS_POST_RATE_OBJ_KEY)
            if not post_rates_dict:
                return dict()
            return json.loads(post_rates_dict)
        except Exception as e:
            self.logger.error(f"function:[get_rate_obj_redis] error:[{e}]")

    def set_rate_obj_redis(self, rates_dict: dict):
        try:
            self.redis.set(settings.REDIS_POST_RATE_OBJ_KEY, json.dumps(rates_dict))
        except Exception as e:
            self.logger.error(f"function:[set_rate_obj_redis] error:[{e}]")

    def process_redis_rates(self):
        try:
            posts_rates_dict = self.get_rate_obj_redis()
            executor = ThreadPoolExecutor(max_workers=settings.RATE_THREAD_POOL_WORKER_COUNT)
            for post_id, rate_list in posts_rates_dict.items():
                try:
                    executor.submit(self.process_post_rate, post_id, rate_list)
                except Exception as e:
                    self.logger.error(
                        f"function:[process_redis_rates] post_id:[{post_id}] rates:[{rate_list}] error:[{e}]")
            self.set_rate_obj_redis(dict())
        except Exception as e:
            self.logger.error(f"function:[process_redis_rates] error:[{e}]")

    def process_post_rate(self, post_id: int, rates: list):
        try:
            post = Post.objects.get_active_by_id(post_id)
            if post.rate_count > settings.MIN_RATE_COUNT_THRESHOLD:
                rate_count = len(rates)
                cycle_rpm = rate_count / settings.RATING_PROCESS_CYCLE_MIN
                average_rpm = post.total_rate / ((post.last_rate_time - post.created_at).total_seconds() / 60)
                growth_index = cycle_rpm / average_rpm
                if growth_index > settings.RATING_GROWTH_INDEX_THRESHOLD:
                    return
            self.bulk_update_or_create_rate(rates)
            self.update_post_rates(post)
        except Exception as e:
            self.logger.error(f"function:[process_post_rate] post_id:[{post_id}] rates:[{rates}] error:[{e}]")

    def update_post_rates(self, post: Post):
        try:
            total_rate, rate_count = Rate.objects.get_sum_and_count(post.id)
            post.total_rate += total_rate
            post.rate_count += rate_count
            post.average_rate = post.total_rate / post.rate_count
            post.last_rate_time = datetime.now()
            post.save()
        except Exception as e:
            self.logger.error(f"function:[update_post_rates] error:[{e}]")

    def bulk_update_or_create_rate(self, rate_list: list):
        try:
            rate_object_list = list()
            for rate in rate_list:
                try:
                    rate_object_list.append(
                        Rate(
                            rater_id=rate['rater_id'],
                            post_id=rate['post_id'],
                            score=rate['score'],
                            created_at=rate['created_at'],
                        )
                    )
                except Exception as e:
                    self.logger.error(f"function:[bulk_update_or_create_rate] rate:[{rate}] error:[{e}]")
            Rate.objects.bulk_update_or_create(
                objs=rate_object_list,
                update_fields=['score'],
                match_field=('post', 'rater',)
            )
        except Exception as e:
            self.logger.error(f"function:[bulk_update_or_create_rate] error:[{e}]")