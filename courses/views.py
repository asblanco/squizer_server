from courses.models import Course, Chapter, Question, Answer
from courses.models import SchoolYear, Call, Test
from courses.serializers import CourseListSerializer, CourseSerializer, ChapterSerializer, QuestionSerializer, AnswerSerializer, QuestionUpdateSerializer
from courses.serializers import SchoolYearSerializer, CallSerializer, TestSerializer
from rest_framework import viewsets
from rest_framework import generics


class CourseList(generics.ListAPIView):
    """
    List all courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

class QuestionUpdate(generics.UpdateAPIView):
    """
    Update question and its answers
    """
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateSerializer

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

class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned tests to a given call and course,
        by filtering against a `call` and `course` query parameter in the URL.
        """
        queryset = Test.objects.all()
        call = self.request.query_params.get('call', None)
        course = self.request.query_params.get('course', None)
        if call is not None:
            queryset = queryset.filter(call=call)
            if course is not None:
                queryset = queryset.filter(course=course)
        return queryset
