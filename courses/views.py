from courses.models import Course, Chapter, Question, Answer
from courses.models import SchoolYear, Call, Test
from courses.serializers import CourseListSerializer, CourseSerializer, ChapterSerializer, QuestionSerializer, AnswerSerializer, QuestionUpdateSerializer
from courses.serializers import SchoolYearSerializer, CallSerializer, TestSerializer, RetrieveTestSerializer
from rest_framework import viewsets
from rest_framework import generics
from squizer_server.settings import BASE_DIR
from django.http import HttpResponse
import os


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

class RetrieveTest(generics.RetrieveAPIView):
    """
    Retrieve test
    """
    queryset = Test.objects.all()
    serializer_class = RetrieveTestSerializer

def pdf_view(request, pk):
    with open(os.path.join(BASE_DIR, 'courses/static/' + pk + '.pdf'), 'rb') as pdf:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=test.pdf'
        return response

def tex_view(request, pk):
    with open(os.path.join(BASE_DIR, 'courses/static/' + pk + '.tex'), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='text/plain')
        response['Content-Disposition'] = 'attachment;filename=' + pk + '.tex'
        return response
