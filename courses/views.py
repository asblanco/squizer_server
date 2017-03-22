from courses.models import Course, Chapter, Question, Answer
from courses.serializers import CourseListSerializer, CourseSerializer, ChapterSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import viewsets
from rest_framework import generics


class CourseList(generics.ListAPIView):
    """
    List all courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer


"""
These viewsets automatically provide `list`, `create`, `retrieve`,
`update` and `destroy` actions.
"""

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
