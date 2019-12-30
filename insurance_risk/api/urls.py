from django.urls import path

from api.views import RiskProfileView


urlpatterns = [
    path('risk-profile', RiskProfileView.as_view(), name='risk-profile')
]
