from rest_framework.routers import DefaultRouter

from ..viewsets import UsersViewSet


router = DefaultRouter()
router.register("", UsersViewSet)


urlpatterns = router.urls
