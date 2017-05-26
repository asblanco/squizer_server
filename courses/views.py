from courses.models import Course, Chapter, Question, Answer, SchoolYear, Call, Test
from courses.serializers import CourseListSerializer, CourseSerializer, ChapterSerializer, QuestionSerializer, AnswerSerializer, QuestionUpdateSerializer
from courses.serializers import SchoolYearSerializer, CallSerializer, TestSerializer, RetrieveTestSerializer
from rest_framework import generics, viewsets
from squizer_server.settings import BASE_DIR
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from random import randint
import codecs, json
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

@api_view(["POST"])
def generateTest(request):
    reader = codecs.getreader("utf-8")
    data = json.load(reader(request))

    test = {
        'id': 0,
        'title': data['title'],
        'course': data['course'],
        'call': data['call'],
        'questions': [],
        'answers': []
    }

    for chapter in data['chapters']:
        if chapter['numberQuestions'] > 0:
            questions = [] # Selected valid questions
            for question in chapter['questions']:
                if question['checked']:
                    q = {
                        'id': question['id'],
                        'answers': []
                    }
                    for answer in question['answers']:
                        if answer['checked']:
                            q['answers'].append(answer['id'])
                    if len(q['answers']) >= 4:
                        questions.append(q)
                    else:
                        return HttpResponseBadRequest('Questions with insufficient selected answers')

            nQuestions = chapter['numberQuestions']
            if len(questions) < nQuestions:
                return HttpResponseBadRequest('Insufficient valid selected questions')
            else:
                while nQuestions > 0:
                    # Select random questions from the pool of selected questions
                    randomIndex = randint(0, len(questions)-1)
                    testQuestion = questions.pop(randomIndex)
                    # Add questions to test
                    test['questions'].append(testQuestion['id'])
                    # Add answers to test, random if there is more than 4 to choose from
                    if len(testQuestion['answers']) > 4:
                        for i in range(0, 4):
                            randomIndex = randint(0, len(testQuestion['answers'])-1)
                            test['answers'].append(testQuestion['answers'].pop(randomIndex))
                    else:
                        for i in range(0, 4):
                            test['answers'].append(testQuestion['answers'].pop())
                    nQuestions -= 1

    return JsonResponse(test)


def retrievePDF(request, pk):
    with open(os.path.join(BASE_DIR, 'courses/static/' + pk + '.pdf'), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=test.pdf'
        return response

def retrieveTEX(request, pk):
    with open(os.path.join(BASE_DIR, 'courses/static/' + pk + '.tex'), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='text/plain')
        response['Content-Disposition'] = 'attachment;filename=' + pk + '.tex'
        return response
