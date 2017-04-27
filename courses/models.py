from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.name


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=100)

    class Meta:
        unique_together = (("id", "course"),)
        ordering = ['id']
    def __str__(self):
        return self.title


class Question(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=500)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("id", "chapter"),)
        ordering = ['id']
    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    title = models.CharField(max_length=1000)
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = (("id", "question"),)
        ordering = ['id']
    def __str__(self):
        return self.title

class SchoolYear(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['end_date']
    def __str__(self):
        return self.title

class Call(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='calls')
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['end_date']
    def __str__(self):
        return self.title
