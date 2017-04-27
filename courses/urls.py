from django.conf.urls import url, include
from courses import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'course', views.CourseViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'school-year', views.SchoolYearViewSet)
router.register(r'call', views.CallViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'^courses/$', views.CourseList.as_view()),
    url(r'^update-question/(?P<pk>[0-9]+)/$', views.QuestionUpdate.as_view()),
    url(r'^', include(router.urls))
]
