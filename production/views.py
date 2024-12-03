from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from .models import Production
from .serializers import (
    ProductionSerializer,
    FullProductionSerializer
)
from rest_framework import status

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProductionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les productions avec des actions CRUD et des données agrégées.
    """
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'date': ['exact'],  # Filtrer par date exacte ou plage de dates
        'format_name': ['exact'],  # Filtrer par nom exact ou partiel (insensible à la casse)
    }
    ordering_fields = ['date', 'quantity']  # Champs triables
    ordering = ['-date']  # Tri par défaut

    @action(detail=False, methods=["get"])
    def aggregates(self, request):
        """
        Endpoint personnalisé pour récupérer les totaux journaliers, cumulés, et pourcentages.
        """
        productions = Production.objects.values('date', 'format_name').annotate(total=Sum('quantity'))

        serializer = FullProductionSerializer(productions, context={"request": request})
        return Response(serializer.data)



class ProductionDeleteByDateViewSet(viewsets.GenericViewSet):
    """
    ViewSet dédié à la suppression des productions par date.
    """

    @action(detail=False, methods=['delete'])
    def delete_by_date(self, request, *args, **kwargs):
        date = request.query_params.get("date")
        if not date:
            return Response(
                {"status": "error", "message": "Date manquante."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Supprimer les productions correspondant à la date donnée
        deleted_count, _ = Production.objects.filter(date=date).delete()
        return Response(
            {
                "status": "success",
                "message": f"{deleted_count} production(s) supprimée(s) pour la date {date}."
            },
            status=status.HTTP_204_NO_CONTENT
        )