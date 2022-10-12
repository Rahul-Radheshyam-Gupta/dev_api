from django.db import models
from core.models import Profile

PENDING = 'Pending'
APPROVED = 'Approved'
REJECTED = 'Rejected'
status_choices = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected')
)

class Category(models.Model):
    category_name = models.CharField(max_length=150)
    created_by = models.ForeignKey(Profile, related_name='categories', on_delete=models.PROTECT)
    status = models.CharField(max_length=100, default=PENDING, choices=status_choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Category - '+self.category_name


class Question(models.Model):
    question_text = models.TextField()
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.PROTECT)
    created_by = models.ForeignKey(Profile, related_name='questions_by_profile', on_delete=models.PROTECT)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    up_vote_list = models.TextField(default="[]")
    down_vote_list = models.TextField(default="[]")
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default=PENDING, choices=status_choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer_text = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.PROTECT)
    created_by = models.ForeignKey(Profile, related_name='answers_by_profile', on_delete=models.PROTECT)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    up_vote_list = models.TextField(default="[]")
    down_vote_list = models.TextField(default="[]")
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


QUESTION = 'Question'
ANSWER = 'Answer'
report_for_choices = (
    (QUESTION, 'Question Reports'),
    (ANSWER, 'Answer Reports')
)
class Report(models.Model):
    report_category = models.CharField(max_length=150)
    feedback = models.TextField(null=True, blank=True)
    report_for = models.CharField(max_length=150, choices=report_for_choices)
    question_id = models.CharField(max_length=10, null=True, blank=True)
    answer_id = models.CharField(max_length=10, null=True, blank=True)
    created_by = models.ForeignKey(Profile, related_name='reports_by_profile', on_delete=models.PROTECT)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_text = models.TextField()
    category = models.ForeignKey(Answer, related_name='comments', on_delete=models.PROTECT)
    created_by = models.ForeignKey(Profile, related_name='comments_by_profile', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


