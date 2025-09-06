from django.urls import path
from .views import GradeListCreateView, GradeDetailView

urlpatterns = [
    path('grades/', GradeListCreateView.as_view(), name='grade-list'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),
]
