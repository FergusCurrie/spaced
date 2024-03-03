from django.db import models
from django.utils import timezone

# Create your models here.

class Atom(models.Model):
    name = models.TextField()
    type = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.name 
    class Meta:  # meta data 
        ordering = ['-created'] # sorting on created? 

class Card(models.Model):
    atom = models.ForeignKey(Atom, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.question + " " + self.answer 
    class Meta:  # meta data 
        ordering = ['-created'] # sorting on created? 

class AtomState(models.Model):
    atom = models.ForeignKey(Atom, on_delete=models.CASCADE) # delete reviews when card deleted
    repetition_number = models.FloatField()
    ease_factor = models.FloatField()
    inter_repetition_interval = models.FloatField()

    def __str__(self):
        return f"{self.atom} {self.repetition_number} {self.ease_factor} {self.inter_repetition_interval}"


class Review(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE) # delete reviews when card deleted
    atom = models.ForeignKey(Atom, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    ease = models.IntegerField()
    def __str__(self):
        return str(self.card) + " " + str(self.ease) + " " + str(self.date)
    class Meta:
        ordering = ['-date'] # sorting on date?