from django.db import models

class Farm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pond(models.Model):
    name = models.CharField(max_length=30)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.farm} - {self.name}'
    
class Hydrophone(models.Model):
    ip = models.GenericIPAddressField()
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pond.name} - {self.ip}'
