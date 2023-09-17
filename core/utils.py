from django.db.models import Sum
from django.db.models.functions import Coalesce
from core.models import Profile
from devian.models import APPROVED, PENDING, REJECTED

def user_added_by_admin(request, profile):
    list_of_setattr_for_value = ['gender', 'contact_number', 'first_name', 'last_name']
    for field_name in list_of_setattr_for_value:
        setattr(profile, field_name, request.data.get(field_name))
    list_of_setattr_for_boolean = ['is_verified', 'is_super_admin']
    for field_name in list_of_setattr_for_boolean:
        setattr(profile, field_name, request.data.get(field_name) == 'true')
    profile.added_by = request.user.profile
    profile.save()


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