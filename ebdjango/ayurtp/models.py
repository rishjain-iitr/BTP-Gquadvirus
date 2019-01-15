from django.db import models

# Create your models here.

class database(models.Model):
    Id = models.CharField(primary_key=True, max_length = 255)
    botanical_name = models.CharField(max_length = 255, blank = True, default = "")
    family = models.CharField(max_length = 255, blank = True, default = "") 
    english_name = models.CharField(max_length = 255, blank = True, default = "") 
    ayurvedic_name = models.CharField(max_length = 255, blank = True, default = "") 
    unani_name = models.CharField(max_length = 255, blank = True, default = "") 
    sidda_tamil_name = models.CharField(max_length = 255, blank = True, default = "") 
    folk_name = models.CharField(max_length = 255, blank = True, default = "") 
    habiatat = models.CharField(max_length = 255, blank = True, default = "") 
    disease = models.CharField(max_length = 255, blank = True, default = "") 
    part = models.CharField(max_length = 255, blank = True, default = "") 
    compound = models.CharField(max_length = 255, blank = True, default = "") 
    references = models.CharField(max_length = 255, blank = True, default = "")