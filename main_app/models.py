from django.db import models
from django.urls import reverse
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Finch(models.Model):
  name = models.CharField(max_length=100)
  breed = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  # Foreignkey for the M:M relationship
  toys = models.ManyToManyField('Toy')

  def __str__(self):
    return self.name

  #redirect to the finch that was just created
  def get_absolute_url(self):
    return reverse('detail', kwargs={'finch_id': self.id})

class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)
  def __str__(self):
    return self.name

class Feeding(models.Model):
  date = models.DateField('feeding date')
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  )
   # Create a finch_id foreign key, use on_delete, when the foreignkey item is deleted, this item would also be deleted
  finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

  def __str__(self):
    # get_sth_display, display the value
    return f"{self.get_meal_display()} on {self.date}"

   # add new method to count feed
  def fed_for_today(self):
    return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

    # sort feeding by date, latest date would be the first
  class Meta:
    ordering = ['-date']
