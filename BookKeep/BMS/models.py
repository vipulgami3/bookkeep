from django.db import models
from BMS.manager import CustomManager
from django.contrib.auth.models import User

your_choices = (
        ('Non-Fiction', u'Non-Fiction'),
        ('Edited', u'Edited'),
        ('Reference', u'Reference'),
        ('Fiction', u'Fiction'),
    )
# Create your models here.
class BookKeep(models.Model):
    user = models.ManyToManyField(User)
    book = models.CharField(max_length = 100)
    author = models.CharField(max_length = 50)
    price = models.FloatField()
    pages = models.IntegerField()
    tbook = models.CharField(max_length = 100, choices=your_choices)
    images = models.ImageField(null=True,upload_to='images/')
    is_deleted = models.CharField(max_length = 2, default = 'n')

    def __str__(self):
        return self.book
    #customObjects = models.Manager()
    myObjects = CustomManager()
