from django.db import models

# Create your models here.

# 仮想Userテーブル
class Publisher(models.Model):
    name = models.CharField(max_length=300)

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

class IdeaTree(models.Model):
    name = models.CharField(max_length=300)
    overview = models.CharField(max_length=300)
    complete_flag = models.IntegerField()
    idea_theme = models.CharField(max_length=300)
    lastidea_id = models.IntegerField()
    passcode = models.CharField(max_length=6, default=True)
    user = models.ForeignKey(Publisher, on_delete=models.CASCADE)

class Element(models.Model):
    name = models.CharField(max_length=300)
    path = models.IntegerField()
    color = models.IntegerField()
    ideatree = models.ForeignKey(IdeaTree, on_delete=models.CASCADE)
    # color 0:textbox 1:類義語 2:しりとり