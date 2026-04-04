from django.db import models

class CalculationLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    medidas = models.CharField(max_length=255)
    orientacion = models.IntegerField(choices=[(1, 'Corto'), (2, 'Largo')], default=2)
    color = models.BooleanField(default=False)
    aislacion = models.BooleanField(default=False)
    superficie = models.FloatField(null=True, blank=True)
    resultado = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.medidas}"
