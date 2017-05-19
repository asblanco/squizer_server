from courses.models import Test, Question, Answer
from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver

from pylatex import Command, Document, Section, Subsection
from pylatex.utils import italic, NoEscape
from squizer_server.settings import BASE_DIR
import os

count = 0
test = None
questions = {}
answers = {}

""" Deletes file from filesystem on `post_delete` """
@receiver(post_delete, sender=Test)
def delete_files(sender, instance, *args, **kwargs):
    path = os.path.join(BASE_DIR, 'courses/static/' + str(instance.id))
    if os.path.isfile(path + '.pdf'):
       os.remove(path + '.pdf')
    if os.path.isfile(path + '.tex'):
       os.remove(path + '.tex')

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

    geometry_options = {"tmargin": "0.5cm"}
    doc = Document('basic', geometry_options=geometry_options)
    doc.documentclass = Command(
        'documentclass',
        options=['12pt'],
        arguments=['exam'],
    )

    doc.preamble.append(Command('title', str(test)))
    doc.preamble.append(Command('author', 'Data Structures and Algorithms'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(r'\hbox to \textwidth{Name:\enspace\hrulefill\hrulefill\hrulefill\enspace ' +
    'Date:\enspace\hrulefill}'))

    doc.append(NoEscape(r'\vspace{0.1in}'))
    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'\fbox{\fbox{\parbox{5.5in}{Answer the questions in the spaces provided on ' +
    'the question sheets. If you run out of room for an answer, continue on the back of the page.}}}'))
    doc.append(NoEscape(r'\addpoints'))
    doc.append(NoEscape(r'\bigskip'))
    doc.append(NoEscape(r'\newline'))
    doc.append(NoEscape(r'\gradetable[h][questions]'))
    doc.append(NoEscape(r'\bigskip'))
    doc.append(NoEscape(r'\end{center}'))

    doc.append(NoEscape(r'\begin{questions}'))
    for q in questions:
        doc.append(NoEscape(r'\question[1]  ' + str(q)))
        doc.append(NoEscape(r'\begin{choices}'))
        for a in answers:
            if a.question == q:
                doc.append(NoEscape(r'\choice ' + a.title))
        doc.append(NoEscape(r'\end{choices}'))
    doc.append(NoEscape(r'\end{questions}'))


    doc.generate_pdf(os.path.join(BASE_DIR, 'courses/static/' + str(test.id)), clean_tex=False)
