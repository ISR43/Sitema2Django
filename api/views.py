from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .serializers import CalculatorRequestSerializer, CalculationLogSerializer
from .services import calcular_pvc
from .models import CalculationLog

def frontend_view(request):
    return render(request, 'index.html')

class CalculatorView(APIView):
    def post(self, request):
        serializer = CalculatorRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                medidas = serializer.validated_data['medidas']
                orientacion = serializer.validated_data.get('orientacion', 2)
                color = serializer.validated_data.get('color', False)
                aislacion = serializer.validated_data.get('aislacion', False)
                
                resultado = calcular_pvc(medidas, orientacion, color, aislacion)
                
                CalculationLog.objects.create(
                    medidas=medidas,
                    orientacion=orientacion,
                    color=color,
                    aislacion=aislacion,
                    superficie=resultado.get('area_total', 0),
                    resultado=resultado
                )
                
                return Response([resultado], status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogsView(APIView):
    def get(self, request):
        logs = CalculationLog.objects.all().order_by('-timestamp')
        serializer = CalculationLogSerializer(logs, many=True)
        return Response(serializer.data)
