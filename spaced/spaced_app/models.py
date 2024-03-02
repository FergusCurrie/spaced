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

class CardState(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE) # delete reviews when card deleted
    repetition_number = models.FloatField()
    ease_factor = models.FloatField()
    inter_repetition_interval = models.FloatField()

    def __str__(self):
        return f"{self.card} {self.repetition_number} {self.ease_factor} {self.inter_repetition_interval}"


class Review(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE) # delete reviews when card deleted
    date = models.DateTimeField(default=timezone.now)
    ease = models.IntegerField()
    def __str__(self):
        return str(self.card) + " " + str(self.ease) + " " + str(self.date)
    class Meta:
        ordering = ['-date'] # sorting on date?