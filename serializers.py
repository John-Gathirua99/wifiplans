from rest_framework import serializers
from .models import WiFiPlan, UserWifiPlan

class WifiPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WiFiPlan
        fields = ['id', 'name', 'speed', 'price']

class UserWifiPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWifiPlan
        fields = ['id', 'user', 'plan', 'start_date', 'end_date']
