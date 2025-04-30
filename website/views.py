from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .models import  Record
from .forms import MaintenanceBannerForm, SignUpForm, AddRecordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url='home')
@permission_required('website.view_record', login_url='home')
def customer_record(request, pk):
    customer_record = Record.objects.get(id=pk)
    return render(request, 'record.html', {'customer_record': customer_record})

@login_required(login_url='home')
@permission_required('website.delete_record', login_url='home')
def delete_record(request, pk):
    delete_it = Record.objects.get(id=pk)
    delete_it.delete()
    messages.success(request, "Record Deleted Successfully...")
    return redirect('home')

@login_required(login_url='home')
@permission_required('website.add_record', login_url='home')
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Record Added...")
            return redirect('home')
    return render(request, 'add_record.html', {'form': form})

@login_required(login_url='home')
@permission_required('website.change_record', login_url='home')
def update_record(request, pk):
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Record Has Been Updated!")
        return redirect('home')
    return render(request, 'update_record.html', {'form': form})

@login_required(login_url='home')
@permission_required('website.add_maintenancebanner', login_url='home')
def create_banner(request):
    if request.method == 'POST':
        form = MaintenanceBannerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MaintenanceBannerForm()
    return render(request, 'createbanner.html', {'form': form})
