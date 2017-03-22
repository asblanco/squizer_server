from django.conf.urls import url, include
from courses import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'course', views.CourseViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'^courses/$', views.CourseList.as_view()),
    url(r'^', include(router.urls))
]
