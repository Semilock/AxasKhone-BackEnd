from rest_framework import routers

from backendMain.viewSets import ProfileViewSet

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet)

urlpatterns = router.urls