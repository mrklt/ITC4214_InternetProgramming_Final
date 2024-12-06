from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, UserProfileForm

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='Users'))  # Add user to 'Users' group
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Administrators').exists())
def admin_page(request):
    # Admin-specific logic here
    return render(request, 'registration/admin_page.html')

def search_items(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    # Add your search logic here based on your Item model
    items = []  # Replace with actual query to your database
    return render(request, 'registration/search_results.html', 
                 {'items': items, 'query': query, 'category': category})
