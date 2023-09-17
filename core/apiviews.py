import json

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from core.serializers import ProfileModelSerializer, GetProfileModelSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from core.models import Profile
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from core.utils import get_profile_stats, user_added_by_admin


class ProfileApiview(GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer

    def create(self, request, *args, **kwargs):
        print("Request Data", request.data)
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        # Validate User
        user_with_username = User.objects.filter(username=username).exists()
        user_with_email = User.objects.filter(email=email).exists()
        if user_with_username or user_with_email:
            duplicate_field_error = f'duplicate user name - {username}' if user_with_username else f'email - {email}'
            raise ValidationError(duplicate_field_error)
        # Create Profile and mapped it with the User
        profile = Profile.objects.create(email=email)
        if profile:
            user = User.objects.create_user(username, email, password)
            profile.user = user
            profile.save()     

        # If admin adds an user then also update user profile
        if request.data.get('added_by_admin', False) == 'true':
            user_added_by_admin(request, profile)            
            print("successfully updated profile..")

        return Response({'success': True}, status=status.HTTP_201_CREATED)


class GetProfileApiview(GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.all()
        is_datatabe_format = self.request.query_params.get('format') == 'datatables'
        if self.request.method == "GET" and not is_datatabe_format:
            queryset = Profile.objects.filter(user=self.request.user)
        return queryset
    serializer_class = GetProfileModelSerializer


class ProfileStatsApiview(ModelViewSet):
    def get_queryset(self):
        queryset = Profile.objects.all()
        for_all_profile = self.request.GET.get('for_all_profile')
        if not for_all_profile:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    serializer_class = ProfileModelSerializer

    def list(self, request, *args, **kwargs):
        profiles = self.get_queryset()
        stats_list = []
        for profile in profiles:
            stats_list.append(get_profile_stats(profile))
        return Response(stats_list, status=200)
