from django.conf.urls import url, include
from courses import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
