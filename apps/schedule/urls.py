from rest_framework.routers import DefaultRouter

from apps.schedule.api import BrixViewSet

router = DefaultRouter()
router.register(r'brix', BrixViewSet, 'brix')
urlpatterns = router.urls