from django.db import models
from django.contrib.auth.models import User

# Create your models here.
result = [
    ('WIN', 'win'),
    ('LOST', 'lost')
]
class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
class TradePhoto(models.Model):
    trade = models.ForeignKey(
        Trade,
        on_delete= models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="photos/")

    def __str__(self):
        return f"Image for {self.trade.pair}"
