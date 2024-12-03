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
