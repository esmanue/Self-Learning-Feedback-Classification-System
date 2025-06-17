from django.urls import path
from .views import PredictOverview
from .views import CorrectLabel

urlpatterns = [
    path("predict/", PredictOverview.as_view()),
    path("feedback/",CorrectLabel.as_view()),
]
