from django.urls import path
from devian import apiviews

category_list = apiviews.CategoryApiview.as_view({
    'get': 'list',
    'post': 'create'
})
category_detail = apiviews.CategoryApiview.as_view({
    'get': 'retrieve',
    'patch': 'update'
})

question_list = apiviews.QuestionApiview.as_view({
    'get': 'list',
    'post': 'create'
})
question_detail = apiviews.QuestionApiview.as_view({
    'get': 'retrieve',
    'patch': 'update'
})

answer_list = apiviews.AnswerApiview.as_view({
    'get': 'list',
    'post': 'create'
})
answer_detail = apiviews.AnswerApiview.as_view({
    'get': 'retrieve',
    'patch': 'update'
})

comment_detail = apiviews.CommentApiview.as_view({
    'get': 'retrieve',
    'patch': 'update'
})
comment_list = apiviews.CommentApiview.as_view({
    'get': 'list',
    'post': 'create'
})

report_detail = apiviews.ReportApiview.as_view({
    'get': 'retrieve',
    'patch': 'update'
})
report_list = apiviews.ReportApiview.as_view({
    'get': 'list',
    'post': 'create'
})

like_dislike_list = apiviews.LikeDislikeCountUpdateView.as_view()
urlpatterns = [
    path('category/', category_list, name='category-list'),
    path('category/<int:pk>/', category_detail, name='category-detail'),
    path('question/', question_list, name='question-list'),
    path('question/<int:pk>/', question_detail, name='question-detail'),
    path('answer/', answer_list, name='answer-list'),
    path('answer/<int:pk>/', answer_detail, name='answer-detail'),
    path('report/', report_list, name='report-list'),
    path('report/<int:pk>/', report_detail, name='report-detail'),
    path('comment/', comment_list, name='comment-list'),
    path('comment/<int:pk>/', comment_detail, name='comment-detail'),
    path('like_dislike/', like_dislike_list, name='like_dislike_list'),
]
