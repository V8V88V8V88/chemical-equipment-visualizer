from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    """Stores uploaded CSV dataset metadata."""
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    file = models.FileField(upload_to='datasets/')

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"


class Equipment(models.Model):
    """Individual equipment record from a CSV row."""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
