from django.urls import path
from .views import RunProgramView

urlpatterns = [
    path('run-program/', RunProgramView.as_view(), name='run-program'),
]
