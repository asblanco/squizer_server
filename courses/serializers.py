from rest_framework import serializers
from courses.models import Course, Chapter, Question, Answer
from django.db import transaction

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
        fields = ('__all__')

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('question',)

class AnswerUpdateSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Answer()._meta.get_field('id'))
    class Meta:
        model = Answer
        exclude = ('question',)
        validators = []

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerCreateSerializer(many=True)

    class Meta:
        model = Question
        validators = []     #unique together validators cannot automatically be applied
        fields = ('__all__')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


class QuestionUpdateSerializer(serializers.ModelSerializer):
    answers = AnswerUpdateSerializer(many=True)
    id = serializers.ModelField(model_field=Question()._meta.get_field('id'))

    class Meta:
        model = Question
        validators = []
        fields = ('__all__')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.title = validated_data.get('title', instance.title)
            instance.save()

            answers_data = validated_data.get('answers')
            for answer in answers_data:
                if answer['id'] != 0:
                    Answer.objects.filter(id = answer['id']).update(title = answer['title'], correct = answer['correct'])

            #Delete answers that were not in the request (the user deleted them)
            old_answers = Answer.objects.filter(question = validated_data.get('id')).values()
            print(old_answers)
            for old in old_answers:
                toDelete = True
                for answer in answers_data:
                    if answer['id'] == old['id']:
                        toDelete = False
                if toDelete:
                    Answer.objects.filter(id=old['id']).delete()

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
