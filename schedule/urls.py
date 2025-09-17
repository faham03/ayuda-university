from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleListView, ScheduleViewSet

# Router pour la gestion complète (admin uniquement)
router = DefaultRouter()
router.register(r'schedule-admin', ScheduleViewSet, basename='schedule-admin')

urlpatterns = [
    # Endpoint par défaut pour les étudiants (consultation avec filtres)
    path('schedule/', ScheduleListView.as_view(), name='schedule-list'),

    # Routes admin (CRUD complet)
    path('', include(router.urls)),
]
