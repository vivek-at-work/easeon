from django.urls import path
from gsx.views import GSXAPIView,GSXAPIMetaView
urlpatterns = [
    path('', GSXAPIMetaView.as_view()),
    path('<str:action>/', GSXAPIView.as_view(),name='gsx_api_endpoint')
]
