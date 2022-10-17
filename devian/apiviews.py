from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import ProfileModelSerializer
from rest_framework.viewsets import ModelViewSet
from devian.models import Category, Question, Answer, Comment, APPROVED, REJECTED, PENDING, Report
from devian.serializers import CategorySerializer, QuestionSerializer, AnswerSerializer, CommentSerializer, \
    ReportSerializer
import json

class CategoryApiview(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        if self.request.method == 'GET':
            is_datatabe_format = self.request.query_params.get('format') == 'datatables'
            if is_datatabe_format:
                status = self.request.query_params.get('status', PENDING)
                queryset = queryset.filter(status=status)
            else:
                queryset = queryset.filter(status=APPROVED)
        return queryset

    # lookup_field = 'id'
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        print("Delete Category ",request.data, args, kwargs)
        category_name = request.data.get('category_name')
        category = Category.objects.create(category_name=category_name, created_by=self.request.user.profile)
        return Response({'success': True}, status=200)

    def update(self, request, *args, **kwargs):
        print("Delete Category ",request.data, args, kwargs)
        action = request.data.get('action')
        category_name = request.data.get('category_name')
        category = Category.objects.get(id=kwargs.get('pk'))
        if action == 'delete':
            category.is_active = False
        elif action == 'update':
            category.category_name = category_name
        elif action in [APPROVED, REJECTED]:
            category.status = action
        category.save()
        return Response({'success': True}, status=204 if action == 'delete' else 200)

class QuestionApiview(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        page_count = self.request.GET.get('question_page_count', None)
        question_id = self.kwargs.get('pk')
        queryset = Question.objects.filter(is_active=True)
        if self.request.method == 'GET':
            category = self.request.GET.get('category')
            if category:
                queryset = queryset.filter(category_id=category)
            search_key = self.request.GET.get('search_key')
            if search_key:
                queryset = queryset.filter(
                    Q(category__category_name__icontains=search_key) |
                    Q(question_text__icontains=search_key)
                )

            is_datatabe_format = self.request.query_params.get('format') == 'datatables'
            if is_datatabe_format:
                status = self.request.query_params.get('status', PENDING)
                queryset = queryset.filter(status=status)
                if not self.request.user.profile.is_super_admin:
                    queryset = queryset.filter(created_by=self.request.user.profile)
            else:
                queryset = queryset.filter(status=APPROVED)

        if page_count and not question_id:
            queryset = queryset.order_by('-created_at')
            page_count = int(page_count)
            start = page_count*5
            end = start+5
            queryset = queryset[start:end]
            print("slice done............", question_id)
        return queryset
    # lookup_field = 'id'
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        question_text = request.data.get('question_text')
        category = request.data.get('category')
        question = Question.objects.create(question_text=question_text, category_id=category, created_by=self.request.user.profile)
        return Response({'success': True}, status=200)

    def update(self, request, *args, **kwargs):
        print("Delete Question ", args, kwargs)
        action = request.data.get('action')
        question = Question.objects.get(id=kwargs.get('pk'))
        if action == 'delete':
            question.is_active = False
        elif action == 'update':
            question.question_text = request.data.get('question_text')
        elif action in [APPROVED, REJECTED]:
            status = request.data.get('status')
            question.status = status

        question.save()
        return Response({'success': True}, status=204 if action == 'delete' else 200)


class AnswerApiview(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Answer.objects.all()
        if self.request.GET.get('question_id'):
            print("====================q a", self.request.method)
            queryset = queryset.filter(question_id=self.request.GET['question_id'], is_active=True)
        if self.request.GET.get('answer_id'):
            queryset = queryset.filter(id=self.request.GET['answer_id'])

        return queryset
    # lookup_field = 'id'
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        answer_text = request.data.get('answer_text')
        question_id = request.data.get('question')
        answer = Answer.objects.create(question_id=question_id, answer_text=answer_text, created_by=self.request.user.profile)
        serializer = self.serializer_class(answer, context={'request': request})
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        print("===============================", request.data)
        action = request.data.get('action')
        answer = Answer.objects.get(id=kwargs.get('pk'))
        if action == 'delete':
            answer.is_active = False
        elif action == 'update':
            answer.answer_text = request.data.get('answer_text')
        answer.save()
        return Response({'success': True, 'answer_text': answer.answer_text}, status=200)

class LikeDislikeCountUpdateView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print("Vote Data ===============>", request.data)
        vote_for = request.data.get('vote_for')
        action = request.data.get('action')
        obj_id = request.data.get('obj_id')
        obj = None
        if vote_for == 'question':
            obj = Question.objects.get(id=obj_id)
        elif vote_for == 'answer':
            obj = Answer.objects.get(id=obj_id)

        up_vote_list = json.loads(obj.up_vote_list)
        down_vote_list = json.loads(obj.down_vote_list)
        if obj:
            if action == 'up':
                if request.user.profile.id not in up_vote_list:
                    up_vote_list.append(request.user.profile.id)
                    if request.user.profile.id in down_vote_list:
                        down_vote_list.remove(request.user.profile.id)
                else:
                    up_vote_list.remove(request.user.profile.id)
            elif action == 'down':
                if request.user.profile.id not in down_vote_list:
                    if request.user.profile.id in up_vote_list:
                        up_vote_list.remove(request.user.profile.id)
                    down_vote_list.append(request.user.profile.id)
                else:
                    down_vote_list.remove(request.user.profile.id)
            obj.up_vote_list = json.dumps(up_vote_list)
            obj.up_votes = len(up_vote_list)
            obj.down_vote_list = json.dumps(down_vote_list)
            obj.down_votes = len(down_vote_list)
            obj.save()
        result = {
            'up_vote_list': obj.up_vote_list,
            'down_vote_list': obj.down_vote_list,
            'up_votes': obj.up_votes,
            'down_votes': obj.down_votes,
            'vote_for': vote_for
        }
        return Response(result, status=201)


class ReportApiview(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Report.objects.all()
        print("aaaaaaaaaaaaaaaa", self.request.GET)
        is_resolved = self.request.GET.get('status') != 'Open'
        queryset = queryset.filter(is_resolved=is_resolved)

        report_for = self.request.GET.get('report_for')
        if report_for:
            queryset = queryset.filter(report_for=report_for)

        if not self.request.user.profile.is_super_admin:
            queryset = queryset.filter(created_by=self.request.user.profile)
        return queryset

    def update(self, request, *args, **kwargs):
        report = Report.objects.get(id=kwargs.get('pk'))
        is_resolved = request.data.get('is_resolved', False) in ['true', 'True', True]
        report.is_resolved = is_resolved
        report.save()
        return Response({'success':True}, status=200)
    serializer_class = ReportSerializer


class CommentApiview(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    # lookup_field = 'id'
    serializer_class = CommentSerializer
