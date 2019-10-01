from rest_framework.routers import DefaultRouter

from apps.schedule.api import BrixViewSet, BrixModulesViewSet

router = DefaultRouter()
router.register(r'brix', BrixViewSet, 'brix')
router.register(r'brix-modules', BrixModulesViewSet, 'brix-modules')
urlpatterns = router.urls