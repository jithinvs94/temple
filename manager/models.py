from django.db import models

# Create your models here.


class Vazhipadu(models.Model):
    vazhipadu_name  = models.CharField(max_length=100, unique=True)
    price           = models.IntegerField()
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.vazhipadu_name



class Data(models.Model):
    vazhipadu = models.ForeignKey(Vazhipadu, on_delete=models.CASCADE)
    count = models.IntegerField()
    person_name = models.CharField(max_length=50)
    nakshathram = models.CharField(max_length=50)
    created_date    = models.DateTimeField(auto_now_add=True)
    just_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.vazhipadu.vazhipadu_name

