from django.urls import path
from core import apiviews
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

profile_list = apiviews.ProfileApiview.as_view({
    'post': 'create'
})
profile_detail = apiviews.ProfileApiview.as_view({
    'patch': 'update'
})

get_profile_stats_list = apiviews.ProfileStatsApiview.as_view({
    'get': 'list',
})

get_profile_list = apiviews.GetProfileApiview.as_view({
    'get': 'list',
})

get_profile_detail = apiviews.GetProfileApiview.as_view({
    'get': 'retrieve',
    'patch': 'update'
})
urlpatterns = [
    path('', profile_list, name='profile-list'),
    path('<int:pk>/', profile_detail, name='profile-detail'),
    path('get_profile/', get_profile_list, name='get-profile-list'),
    path('get_profile/<int:pk>/', get_profile_detail, name='get-profile-detail'),
    path('profile_stats/', get_profile_stats_list, name='profile-stats'),
    # JWT Token End Points
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



