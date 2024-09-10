from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import WiFiPlan
from .forms import WiFiPlanForm,PaymentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import JsonResponse
from .mpesa_integration import initiate_payment
from rest_framework.response import Response
from django.contrib import messages

# import plans.json
import json
from django.views.generic import DeleteView,DetailView,ListView
# List all WiFi plans

import requests
from requests.exceptions import HTTPError

def wifi_plans_list(request):
    plans = WiFiPlan.objects.all()
  

    return render(request, 'app1/plan_list.html', {'plans': plans})

# Display details of a specific WiFi plan
@login_required
def plan_detail(request,pk):
    # plan = get_object_or_404(WiFiPlan, id=pk)

    # amount = request.POST.get('amount')
    plan = WiFiPlan.objects.get(id=pk)
    return render(request, 'app1/plan_detail.html', {'plan': plan})

class PlanDetail(LoginRequiredMixin,DetailView):
    model = WiFiPlan
    context_object_name='plans'
    template_name='app1/plan_detail.html'

# Create a new WiFi plan
@login_required
def plan_create(request):
    if request.method == 'POST':
        form = WiFiPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_list')
    else:
        form = WiFiPlanForm()
    return render(request, 'app1/plan_form.html', {'form': form})



class PlanDelete(LoginRequiredMixin,DeleteView):
    model = WiFiPlan
    template_name = 'app1/plan_delete.html'
    success_url='/'





# mpesa integration



def initiate_payment_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        response = initiate_payment(amount, phone_number)
        # return JsonResponse(response)
        return render(request,'app1/mpesa_confirmation.html')
    return render(request, 'app1/mpesa_form.html')



from rest_framework import viewsets
from .models import WiFiPlan, UserWifiPlan
from .serializers import WifiPlanSerializer, UserWifiPlanSerializer



class WifiPlanViewSet(viewsets.ModelViewSet):
    queryset = WiFiPlan.objects.all()
    serializer_class = WifiPlanSerializer


class UserWifiPlanViewSet(viewsets.ModelViewSet):
    queryset = UserWifiPlan.objects.all()
    serializer_class = UserWifiPlanSerializer



def purchase_plan(request, plan_id):
    plan = get_object_or_404(WiFiPlan, id=plan_id)
    # Implement payment logic here
    # After payment, activate the plan
    if activate_plan_on_router(plan):
        messages.success(request, 'Plan activated successfully!')
    else:
        messages.error(request, 'Failed to activate plan.')
    return redirect('wifi-plans-list')

def activate_plan_on_router(plan):
    # Logic to interface with the router or manage user access
    # For example, send an API request to the router to set up the plan
    return True


def update_router_config(plan):
    api_url = 'http://router_ip/api/config'
    payload = {
        'plan_name': plan.name,
        'speed': plan.speed,
        'data_limit': plan.data_limit,
    }
    response = requests.post(api_url, json=payload, auth=('admin', 'password'))
    return response.status_code == 200