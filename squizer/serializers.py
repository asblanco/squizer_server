from rest_framework import serializers
from squizer.models import Course, Chapter, Question, Answer, SchoolYear, Term, Test
from django.db import transaction

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')

# Field question is excluded because when creating a question it doesnt know the value
class AnswerDetailSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Answer()._meta.get_field('id'))
    class Meta:
        model = Answer
        fields = ('id', 'title', 'correct')

class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    Question Writable Nested Serializer to Update and Create Questions with Answers,
    Retrieve question details for course-detail and Delete a question
    """
    answers = AnswerDetailSerializer(many=True)
    # The request needs to send always an id, even in create, I will ignore it
    id = serializers.ModelField(model_field=Question()._meta.get_field('id'))

    class Meta:
        model = Question
        validators = []     #unique together validators cannot automatically be applied, the angular app is sending all id=0, so it is not unique
        fields = ('__all__')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        # avoid dummy id, create the question
        question = Question.objects.create(title=validated_data['title'], chapter=validated_data['chapter'])
        # Save the answers of the new question
        for answer_data in answers_data:
            Answer.objects.create(title=answer_data['title'], correct=answer_data['correct'], question=question)
        return question

    def update(self, instance, validated_data):
        with transaction.atomic():
            # Update title of the question
            instance.title = validated_data.get('title', instance.title)
            instance.save()

            answers_data = validated_data.get('answers')
            #Delete answers that were not in the request (the user deleted them)
            old_answers = Answer.objects.filter(question = validated_data.get('id')).values()
            for old in old_answers:
                toDelete = True
                for answer in answers_data:
                    if answer['id'] == old['id']:
                        toDelete = False
                if toDelete:
                    Answer.objects.filter(id=old['id']).delete()

            # Update and Create answers
            for answer in answers_data:
                if answer['id'] != 0:
                    Answer.objects.filter(id = answer['id']).update(title = answer['title'], correct = answer['correct'])
                else:
                    Answer.objects.create(title=answer['title'], correct=answer['correct'], question=instance)

            return instance

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

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('__all__')

class SchoolYearListSerializer(serializers.ModelSerializer):
    terms = TermSerializer(many=True)
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
