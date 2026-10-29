from django.db import models

class Mesa(models.Model):
    nombre = models.TextField(max_length=100)
    def __str__(self):
        return self.name