from rest_framework import serializers
from courses.models import Course, Chapter, Question, Answer, SchoolYear, Call, Test
from drf_writable_nested import WritableNestedModelSerializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')

# Field question is excluded because when creating a question it doesnt know the value
class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'title', 'correct')

class QuestionDetailSerializer(WritableNestedModelSerializer):
    """
    Question Writable Nested Serializer to Update and Create Questions with Answers,
    Retrieve question details for course-detail and Delete a question
    """
    answers = AnswerDetailSerializer(many=True)
    class Meta:
        model = Question
        fields = ('__all__')

class ChapterDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True)
    class Meta:
        model = Chapter
        fields = ('__all__')

class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Nested Serializers to retrieve a Course's Details
    """
    chapters = ChapterDetailSerializer(many=True)
    class Meta:
        model = Course
        fields = ('id', 'name', 'chapters')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('__all__')

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ('__all__')

class SchoolYearListSerializer(serializers.ModelSerializer):
    calls = CallSerializer(many=True)
    class Meta:
        model = SchoolYear
        fields = ('__all__')

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ('__all__')

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('__all__')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('__all__')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('__all__')

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Test
        fields = ('__all__')
        depth = 1
