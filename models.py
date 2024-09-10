from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
class WiFiPlan(models.Model):
    name = models.CharField(max_length=100)
    speed = models.CharField(max_length=50)
    data_limit = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
    def get_absolute_url(self):

        return reverse('plan_detail',kwargs={'pk':self.pk})


class UserWifiPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(WiFiPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()