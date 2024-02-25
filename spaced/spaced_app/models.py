from django.db import models
from django.utils import timezone

# Create your models here.

class Card(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.question + " " + self.answer 
    class Meta:  # meta data 
        ordering = ['-created'] # sorting on created? 


class Review(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE) # delete reviews when card deleted
    date = models.DateTimeField(default=timezone.now)
    ease = models.IntegerField()
    def __str__(self):
        return str(self.card) + " " + str(self.ease) + " " + str(self.date)
    class Meta:
        ordering = ['-date'] # sorting on date?