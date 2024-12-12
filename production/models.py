from django.db import models

class Production(models.Model):
    date = models.DateField()  # Date de la production
    format_name = models.CharField(max_length=100)  # Nom du format
    quantity = models.PositiveIntegerField()  # Quantité produite

    class Meta:
        verbose_name = "Production"
        verbose_name_plural = "Productions"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.format_name}: {self.quantity}"


class Stock(models.Model):
    date = models.DateField()
    film = models.CharField(max_length=100)
    entry = models.FloatField()
    machine1 = models.FloatField()
    machine2 = models.FloatField()
    daily_total = models.FloatField()
    gaspiage = models.FloatField()
    stock_initial = models.FloatField()
    stock_cumule = models.FloatField()

    def save(self, *args, **kwargs):
        previous_data = Stock.objects.filter(date=self.date).first()
        self.stock_initial = previous_data.stock_cumule if previous_data else 0
        used = self.daily_total * 0.005 * 20
        total_m1_m2 = (self.machine1 + self.machine2) * 0.005
        self.gaspiage = round(total_m1_m2 - used, 2)
        self.stock_cumule = self.stock_initial + self.entry - self.gaspiage - used
        super().save(*args, **kwargs)

