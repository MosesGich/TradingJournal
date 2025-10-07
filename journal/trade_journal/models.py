from django.db import models

# Create your models here.
result = [
    ('WIN', 'win'),
    ('LOST', 'lost')
]
class Trade(models.Model):
    image = models.ImageField(upload_to="photos/")
    outcome = models.CharField(
        max_length=4,
        choices=result,
        default="WIN",
        verbose_name="outcome"

    )
    pair = models.CharField(max_length=6)
    profit = models.IntegerField()
    date = models.DateField(blank=False)
    notes = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pair} {self.profit} {self.outcome}"