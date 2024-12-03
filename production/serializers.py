from rest_framework import serializers
from .models import Production

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'date', 'format_name', 'quantity']


class DailyTotalsSerializer(serializers.Serializer):
    date = serializers.DateField()
    formats = serializers.DictField(child=serializers.IntegerField())
    total = serializers.IntegerField()


class CumulativeTotalsSerializer(serializers.Serializer):
    format_name = serializers.CharField()
    total_quantity = serializers.IntegerField()


class PercentagesSerializer(serializers.Serializer):
    format_name = serializers.CharField()
    percentage = serializers.FloatField()


class FullProductionSerializer(serializers.Serializer):
    daily_totals = serializers.SerializerMethodField()
    cumulative_totals = serializers.SerializerMethodField()
    total_global = serializers.SerializerMethodField()
    percentages = serializers.SerializerMethodField()

    def get_daily_totals(self, productions):
        daily_totals = {}
        for prod in productions:
            date = prod['date'].strftime('%Y-%m-%d')
            format_name = prod['format_name']
            quantity = prod['total']

            if date not in daily_totals:
                daily_totals[date] = {"formats": {}, "total": 0}

            daily_totals[date]["formats"][format_name] = quantity
            daily_totals[date]["total"] += quantity

        return [
            {"date": date, "formats": values["formats"], "total": values["total"]}
            for date, values in daily_totals.items()
        ]

    def get_cumulative_totals(self, productions):
        cumulative_totals = {}
        for prod in productions:
            format_name = prod['format_name']
            quantity = prod['total']

            if format_name not in cumulative_totals:
                cumulative_totals[format_name] = 0
            cumulative_totals[format_name] += quantity

        return [
            {"format_name": format_name, "total_quantity": total}
            for format_name, total in cumulative_totals.items()
        ]

    def get_total_global(self, productions):
        return sum(prod['total'] for prod in productions)

    def get_percentages(self, productions):
        cumulative_totals = {}
        total_global = self.get_total_global(productions)

        for prod in productions:
            format_name = prod['format_name']
            quantity = prod['total']

            if format_name not in cumulative_totals:
                cumulative_totals[format_name] = 0
            cumulative_totals[format_name] += quantity

        return [
            {
                "format_name": format_name,
                "percentage": round((quantity / total_global) * 100, 2) if total_global > 0 else 0
            }
            for format_name, quantity in cumulative_totals.items()
        ]
