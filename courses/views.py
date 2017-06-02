from courses.models import Course, Chapter, Question, Answer, SchoolYear, Call, Test
from courses.serializers import CourseSerializer, CourseDetailSerializer, ChapterSerializer, QuestionDetailSerializer
from courses.serializers import SchoolYearListSerializer, SchoolYearSerializer, CallSerializer, TestDetailSerializer, TestSerializer
from rest_framework import generics, viewsets
from squizer_server.settings import BASE_DIR
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from random import randint
import codecs, json
import os

class CourseViewSet(viewsets.ModelViewSet):
    """
    List, Retrieve, Create, List, Update and Destroy a Course
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def get_queryset(self):
        """
        Filters the list of courses for the currently authenticated user.
        """
        user = self.request.user
        return Course.objects.filter(teachers=user)

    def perform_create(self, serializer):
        return serializer.save(teachers=[1, self.request.user])

class CourseDetail(generics.RetrieveAPIView):
    """
    Retrieve Course with extended details
    """
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    """
    Used to Create, Update and Delete Chapters,
    and also Retrieve in the browsable Django REST API
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer

class SchoolYearList(generics.ListAPIView):
    """
    Returns the list with School Years and its Calls
    """
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearListSerializer

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

class TestDetail(generics.RetrieveAPIView):
    """
    Retrieve extended Test details
    """
    queryset = Test.objects.all()
    serializer_class = TestDetailSerializer


@api_view(["POST"])
def generateTest(request):
    reader = codecs.getreader("utf-8")
    data = json.load(reader(request))

    # Test to be saved to database
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
            selectedQuestions = []
            # Store selected/checked valid questions in selectedQuestions
            for question in chapter['questions']:
                if question['checked']:
                    q = {
                        'id': question['id'],
                        'answers': []
                    }
                    # Append checked answers to q
                    corrects, incorrects = 0, 0
                    for answer in question['answers']:
                        if answer['checked']:
                            if answer['correct']:
                                corrects += 1
                            else:
                                incorrects += 1
                            a = {
                                'id': answer['id'],
                                'correct': answer['correct']
                            }
                            q['answers'].append(a)
                    # Only store q in selectedQuestions if there are at least 1 correct and 3 incorrect answers checked
                    if corrects >= 1 and incorrects >= 3:
                        selectedQuestions.append(q)
                    else:
                        return HttpResponseBadRequest('Question ' + str(q['id']) + ' with insufficient selected answers. At least 1 correct and 3 incorrects')

            # If the user wants a test with more questions that the actual number of valid selected questions
            testNQuestions = chapter['numberQuestions']
            if len(selectedQuestions) < testNQuestions:
                return HttpResponseBadRequest('Insufficient number of valid selected questions')
            else:
                while testNQuestions > 0:
                    # Select random questions from the pool of selected questions
                    randomIndex = randint(0, len(selectedQuestions)-1)
                    testQuestion = selectedQuestions.pop(randomIndex)
                    # Add questions to test
                    test['questions'].append(testQuestion['id'])

                    # Add answers to test, random if there is more than 4 to choose from
                    if len(testQuestion['answers']) > 4:
                        answersAdded, correct, incorrect = 0, 0, 0
                        # Choose 4 answers
                        while (answersAdded <= 4) and (len(testQuestion['answers']) > 0):
                            randomIndex = randint(0, len(testQuestion['answers'])-1)
                            answer = testQuestion['answers'].pop(randomIndex)
                            # Add only 1 correct and 3 incorrects
                            if not answer['correct'] and incorrect < 3:
                                test['answers'].append(answer['id'])
                                incorrect += 1
                                answersAdded += 1
                            elif answer['correct'] and correct == 0:
                                test['answers'].append(answer['id'])
                                correct += 1
                                answersAdded += 1
                    else:
                        for i in range(0, 4):
                            test['answers'].append(testQuestion['answers'].pop())
                    testNQuestions -= 1

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
