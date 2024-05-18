from django.urls import path

from apps.rate.api.v1.views import RateView

urlpatterns = [
    path('', RateView.as_view(), name='rate_view'),
]
