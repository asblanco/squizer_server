from django.conf.urls import url, include
from squizer import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'course', views.CourseViewSet)
router.register(r'chapter', views.ChapterViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'schoolyear', views.SchoolYearViewSet)
router.register(r'term', views.TermViewSet)
router.register(r'test', views.TestViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'^course-detail/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view()),
    url(r'^schoolyears/$', views.SchoolYearList.as_view()),
    url(r'^test-detail/(?P<pk>[0-9]+)/$', views.TestDetail.as_view()),
    url(r'^test-pdf/(?P<pk>[0-9]+)/$', views.retrievePDF),
    url(r'^test-tex/(?P<pk>[0-9]+)/$', views.retrieveTEX),
    url(r'^generate-test/$', views.generateTest),
    url(r'^api-token-auth/', obtain_jwt_token),
] + router.urls
