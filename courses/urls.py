from django.conf.urls import url, include
from courses import views
from rest_framework.routers import DefaultRouter
from django.conf import settings

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'answer', views.AnswerViewSet)
router.register(r'call', views.CallViewSet)
router.register(r'chapter', views.ChapterViewSet)
router.register(r'course', views.CourseViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'school-year', views.SchoolYearViewSet)
router.register(r'test', views.TestViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'^courses/$', views.CourseList.as_view()),
    url(r'^update-question/(?P<pk>[0-9]+)/$', views.QuestionUpdate.as_view()),
    url(r'^retrieve-test/(?P<pk>[0-9]+)/$', views.RetrieveTest.as_view()),
    url(r'^', include(router.urls))
]

if not settings.DEBUG:
    urlpatterns += url('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))
