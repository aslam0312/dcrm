from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import MaintenanceBanner
from .forms import MaintenanceBannerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Role check helpers
def is_tech(user):
    return user.groups.filter(name='Tech').exists()

def is_member(user):
    return user.groups.filter(name='Member').exists()

def is_admin(user):
    return user.is_superuser

def home(request):
    records = Record.objects.all()
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
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
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated and (is_tech(request.user) or is_admin(request.user)):
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You dont have permission to view this page...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated and is_admin(request.user):
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.error(request, "You Do Not Have Permission To Delete Records...")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated and (is_tech(request.user) or is_admin(request.user)):
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You Do Not Have Permission To Add Records...")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated and (is_tech(request.user) or is_admin(request.user)):
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "You Do Not Have Permission To Update Records...")
        return redirect('home')


def is_not_tech_or_admin(user):
    return user.groups.filter(name__in=['Member']).exists()

@login_required(login_url='home')  # Redirects to login if not logged in
@user_passes_test(is_not_tech_or_admin, login_url='home')  # Redirects to home if not Tech/Admin
def create_banner(request):
    if request.method == 'POST':
        form = MaintenanceBannerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MaintenanceBannerForm()
    return render(request, 'createbanner.html', {'form': form})