from rest_framework.routers import DefaultRouter

from apps.schedule.api import BrixViewSet, BrixModulesViewSet, CommonViewSet

router = DefaultRouter()
router.register(r'brix', BrixViewSet, 'brix')
router.register(r'common', CommonViewSet, 'common')
router.register(r'brix-modules', BrixModulesViewSet, 'brix-modules')
urlpatterns = router.urls