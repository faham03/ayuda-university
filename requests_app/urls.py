from django.urls import path
from .views import StudentRequestListCreateView, AdminRequestListView, AdminRequestUpdateView

urlpatterns = [
    path('student/', StudentRequestListCreateView.as_view(), name='student_requests'),
    path('admin/', AdminRequestListView.as_view(), name='admin_requests'),
    path('admin/<int:pk>/', AdminRequestUpdateView.as_view(), name='admin_request_update'),
]
