from core.serializers import GetProfileModelSerializer
from devian.models import Category, Question, Answer, Comment, Report
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='get-profile-detail')
    first_name = serializers.CharField(source='created_by.first_name', read_only=True)
    last_name = serializers.CharField(source='created_by.last_name', read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Question Serializer"""
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='question-detail')
    is_active = serializers.BooleanField(default=True, required=False)
    pin_answer = serializers.SerializerMethodField(read_only=True)
    pin_answer = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    created_by = GetProfileModelSerializer()
    class Meta:
        model = Question
        fields = '__all__'

    def get_pin_answer(self, obj):
        answers = obj.answers.filter(is_active=True)
        pin_answer_dict = {'no_answer': True}
        if answers:
            answer = answers.order_by('-up_votes').first()
            pin_answer_dict['id'] = answer.id
            pin_answer_dict['no_answer'] = False
            pin_answer_dict['answer_count'] = answers.count()
            pin_answer_dict['answer_text'] = answer.answer_text
            pin_answer_dict['answer_by'] = (answer.created_by.first_name+' '+answer.created_by.last_name) if answer.created_by.first_name else answer.created_by.user.username
            pin_answer_dict['created_at'] = answer.created_at
        return pin_answer_dict


class AnswerSerializer(serializers.ModelSerializer):
    """Answer Serializer"""
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='answer-detail')
    is_active = serializers.BooleanField(default=True, required=False)
    question_id = serializers.CharField(source='question.id', read_only=True)
    created_by = GetProfileModelSerializer()

    class Meta:
        model = Answer
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    """Report Serializer"""
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='report-detail')
    first_name = serializers.CharField(source='created_by.first_name', read_only=True)
    last_name = serializers.CharField(source='created_by.last_name', read_only=True)
    class Meta:
        model = Report
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer"""
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='comment-detail')

    class Meta:
        model = Comment
        fields = '__all__'
