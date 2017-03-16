from rest_framework import serializers
from courses.models import Course, Chapter, Question, Answer

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
            inv_item = Question.objects.get(question=question, pk=item.pk)
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
            inv_item = Chapter.objects.get(chapter=chapter, pk=item.pk)
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
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        items = validated_data.get('chapters')
        for item in items:
            inv_item = Course.objects.get(course=course, pk=item.pk)
            inv_item.save()

        instance.save()
        return instance
