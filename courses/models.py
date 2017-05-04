from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (("id", "course"),)
        ordering = ['id']


class Question(models.Model):
    title = models.CharField(max_length=500)
    last_modified = models.DateField(auto_now=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (("id", "chapter"),)
        ordering = ['id']


class Answer(models.Model):
    title = models.CharField(max_length=1000)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (("id", "question"),)
        ordering = ['id']

class SchoolYear(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['end_date']

class Call(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='calls')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['end_date']

class Test(models.Model):
    title = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='tests')
    questions = models.ManyToManyField(Question)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['creation_date']
