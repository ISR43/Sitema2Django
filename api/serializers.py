from rest_framework import serializers
from .models import CalculationLog

class CalculatorRequestSerializer(serializers.Serializer):
    medidas = serializers.CharField(help_text="Ejemplo: '8*8+9*9'")
    orientacion = serializers.IntegerField(required=False, default=2, help_text="1 para Paralelo al lado CORTO, 2 para Paralelo al lado LARGO")
    color = serializers.BooleanField(required=False, default=False, help_text="¿Desea PVC a Color?")
    aislacion = serializers.BooleanField(required=False, default=False, help_text="¿Desea agregar Aislación Térmica (Lana de vidrio)?")

class CalculationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationLog
        fields = '__all__'
