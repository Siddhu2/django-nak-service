from django.shortcuts import render, redirect, get_object_or_404
from .models import service
from .forms import serviceForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from django.conf import settings  

# Create your views here.
def home(request):
    return render(request, 'service/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'service/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'service/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request,user)
            return redirect('currentservice')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createservice(request):
    if request.method == 'GET':
        return render(request, 'service/createservice.html',{'form':serviceForm()})
    else:
        try:
            form = serviceForm(request.POST)
            newservice = form.save(commit=False)
            newservice.save()
            return redirect('currentservice')
        except:
            return render(request, 'service/createservice.html', {'form':serviceForm(), 'error':'Bad data passed in'})

@login_required
def currentservice(request):
    services = service.objects.filter(datecompleted__isnull=True)
    return render(request, 'service/currentservice.html', {'services':services})

@login_required
def completedservice(request):
    services = service.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'service/completedservice.html', {'services':services})

@login_required
def viewservice(request, service_pk):
    services = get_object_or_404(service,pk=service_pk)
    if request.method == 'GET':
        form = serviceForm(instance=services)
        return render(request, 'service/viewservice.html', {'service':services, 'form':form})
    else:
        try:
            form = serviceForm(request.POST, instance=services)
            form.save()
            return redirect('currentservice')
        except ValueError:
            return render(request, 'service/viewservice.html', {'service':services, 'form':form, 'error': 'Bad info'})

@login_required
def completeservice(request, service_pk):
    services = get_object_or_404(service, pk=service_pk)
    if request.method == 'POST':
        item=services.item
        message_to_broadcast = "உங்கள் "+item+" சரி செய்யப்பட்டது"
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        mobile = "+919488988481"
        client.messages.create(to=mobile,from_=settings.TWILIO_NUMBER,body=message_to_broadcast)
        services.datecompleted = timezone.now()
        services.save()
        return redirect('currentservice')

@login_required
def deleteservice(request, service_pk):
    services = get_object_or_404(service, pk=service_pk)
    if request.method == 'POST':
        services.delete()
        return redirect('currentservice')