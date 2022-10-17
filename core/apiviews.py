import json

from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated

from core.serializers import ProfileModelSerializer, GetProfileModelSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from core.models import Profile
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError

from devian.models import APPROVED, REJECTED, PENDING

profile_ranks = {
    '1': [5, 5],
    '2': [10, 10],
    '3': [20, 30],
    '4': [35, 50],
    '5': [50, 60],
}


def get_profile_stats(profile):
    """
    This function takes profile object as parameter and return profile stats along with the basic detail of
    the passed profile object.
    """
    questions = profile.questions_by_profile.filter(is_active=True)
    answers = profile.answers_by_profile.filter(is_active=True)
    reports = profile.reports_by_profile.all()
    up_votes_count = questions.aggregate(up_vote_count=Coalesce(Sum('up_votes'), 0))['up_vote_count']
    down_votes_count = questions.aggregate(down_vote_count=Coalesce(Sum('down_votes'), 0))['down_vote_count']
    result = {
        'profile_id':profile.id,
        'profile_name': profile.first_name+' '+profile.last_name,
        'rank': profile.rank,
        'question': {
            'total': questions.count(),
            'approved': questions.filter(status=APPROVED).count(),
            'pending': questions.filter(status=PENDING).count(),
            'rejected': questions.filter(status=REJECTED).count(),
            'up_votes': up_votes_count,
            'down_votes': down_votes_count,
        },
        'answer': {
            'total': answers.count(),
            'approved': answers.count()
        },
        'report': {
            'total': reports.count(),
            'closed': reports.filter(is_resolved=True).count(),
            'open': reports.filter(is_resolved=False).count()
        }
    }
    return result


def update_profile_rank(profile_id=None):
    """
    This function needs to be run weekly to update rank of all active profiles.
    If you want to update rank of a profile manually then you need to profile id.
    """
    profiles = Profile.objects.filter(is_active=True)
    if profile_id:
        profiles = profiles.filter(id=profile_id)
    for profile in profiles:
        profile_stats_dict = get_profile_stats(profile)
        total_approved_question = profile_stats_dict['question']['approved']
        total_approved_answer = profile_stats_dict['answer']['approved']
        rank = '1st'
        if total_approved_question < 5 and total_approved_answer < 5:
            rank = '1st'
        elif total_approved_question < 10 and total_approved_answer < 10:
            rank = '2nd'
        elif total_approved_question < 20 and total_approved_answer < 30:
            rank = '3rd'
        elif total_approved_question < 35 and total_approved_answer < 50:
            rank = '4th'
        elif total_approved_question < 50 and total_approved_answer < 60:
            rank = '5th'
        profile.rank = rank
        profile.save()

# class ProfileApiview(ModelViewSet):
#     queryset = Profile.objects.all()
#     # lookup_field = 'id'
#     serializer_class = ProfileModelSerializer


class ProfileApiview(GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer

    def create(self, request, *args, **kwargs):
        print("Request Data", request.data)
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        user_with_username = User.objects.filter(username=username).exists()
        user_with_email = User.objects.filter(email=email).exists()
        if user_with_username or user_with_email:
            duplicate_field_error = f'user name - {username}' if user_with_username else f'email - {email}'
            raise ValidationError(duplicate_field_error)
        profile = Profile.objects.create(email=email)
        if profile:
            user = User.objects.create_user(username, email, password)
            profile.user = user
            profile.save()
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
    # permission_classes = (IsAuthenticated,)

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
            # update_profile_rank(profile.id)
            stats_list.append(get_profile_stats(profile))
        return Response(stats_list, status=200)
