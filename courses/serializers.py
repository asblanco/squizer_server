from rest_framework import serializers
from courses.models import Course, Chapter, Question, Answer

"""
Serializer for courses list
"""

class CourseListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)


"""
ModelSerializers with writable nested serializers
"""

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'id', 'title', 'correct')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ('chapter', 'id', 'title', 'answers')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **chapter_data)
        return question

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        items = validated_data.get('answers')
        for item in items:
            inv_item = Answer.objects.get(question=item['question'], title=item['title'])
            inv_item.save()

        instance.save()
        return instance


class ChapterSerializer(serializers.ModelSerializer):
    #course = serializers.ReadOnlyField(source='course.id')
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Chapter
        fields = ('course', 'id', 'title', 'questions')

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        chapter = Chapter.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(course=course, **question_data)
        return chapter

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        items = validated_data.get('questions')
        for item in items:
            inv_item = Question.objects.get(chapter=item['chapter'], title=item['title'])
            inv_item.save()

        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'chapters')

    def create(self, validated_data):
        chapters_data = validated_data.pop('chapters')
        course = Course.objects.create(**validated_data)
        for chapter_data in chapters_data:
            Chapter.objects.create(course=course, **chapter_data)
        return course

    def update(self, instance, validated_data):
        """
        Update only the name of the course (not chapters)
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
