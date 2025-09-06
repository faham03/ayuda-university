from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleListView, ScheduleViewSet

# Router pour la gestion complète (admin)
router = DefaultRouter()
router.register(r'schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [
    # Endpoint pour les étudiants (consultation avec filtres)
    path('schedule/list/', ScheduleListView.as_view(), name='schedule-list'),

    # On inclut les routes automatiques du ViewSet (CRUD complet pour admin)
    path('', include(router.urls)),
]
