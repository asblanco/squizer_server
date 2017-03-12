from courses.models import Course
from courses.serializers import CourseSerializer
from rest_framework import viewsets


class CourseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
