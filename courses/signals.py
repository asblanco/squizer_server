from courses.models import Test, Question, Answer
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from pylatex import Document, Section, Subsection
from pylatex.utils import italic
from squizer_server.settings import BASE_DIR
import os

count = 0
test = None
questions = {}
answers = {}

@receiver(m2m_changed, sender=Test.questions.through)
def prepare_questions(sender, instance, action, pk_set, **kwargs):
    global count, questions, answers, test

    if action == "post_add":
        questions = {}
        test = instance
        count += 1
        if count == 3:
            count = 1
        questions = instance.questions.all()

        if count == 2:
            generate_pdf()

@receiver(m2m_changed, sender=Test.answers.through)
def prepare_answers(sender, instance, action, pk_set, **kwargs):
    global count, questions, answers, test

    if action == "post_add":
        answers = {}
        count += 1
        if count == 3:
            count = 1
        answers = instance.answers.all()

        if count == 2:
            generate_pdf()

def generate_pdf():
    global questions, answers, test
    geometry_options = {"tmargin": "1cm", "lmargin": "2cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section(test)):
        doc.append('Answer all the questions you can. Good luck!')
        for q in questions:
            with doc.create(Subsection(q)):
                for a in answers:
                    if a.question == q:
                        doc.append('- ' + a.title + ' \n')


    doc.generate_pdf(os.path.join(BASE_DIR, 'courses/static/' + str(test.id)), clean_tex=False)
