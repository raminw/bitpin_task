from django.core.management.base import BaseCommand

from apps.rate.services import RateService


class Command(BaseCommand):
    help = 'Process Post Rates'

    def handle(self, *args, **options):
        RateService().process_redis_rates()
