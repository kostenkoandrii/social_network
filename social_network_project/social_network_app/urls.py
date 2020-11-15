from rest_framework import routers

from .views import SimplePostViewSet, LikeAnalyticsViewSet, LikeViewSet, UserActivityViewSet

router = routers.DefaultRouter()
router.register(r'post', SimplePostViewSet, 'post')
router.register(r'like', LikeViewSet, 'like')
router.register(r'like_analytics', LikeAnalyticsViewSet, 'like_analytics')
router.register(r'user_activity', UserActivityViewSet, 'user_activity')

urlpatterns = router.urls
