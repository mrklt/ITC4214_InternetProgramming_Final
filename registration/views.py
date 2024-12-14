from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, UserProfileForm
from products.models import Item
from .forms import ItemForm


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                group = Group.objects.get(name='Users')  # Replace with the desired group name
                user.groups.add(group)
            except Group.DoesNotExist:
                # Handle the case where the group doesn't exist
                messages.error(request, 'User group does not exist. Please create it.')
                return redirect('home')  # Redirect to home or another appropriate page
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
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
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page

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

@login_required
def manage_items(request):
    if not request.user.is_creator:
        return redirect('home') 

    items = Item.objects.all()

    if request.method == 'POST':
        # Handle the form submission
        item_id = request.POST.get('item_id')
        new_price = request.POST.get('price')

        # Get the item and update its price
        item = get_object_or_404(Item, id=item_id)
        item.price = new_price
        item.save()

      
        messages.success(request, f"Price for '{item.name}' updated successfully!")

        return redirect('manage_items')

    return render(request, 'registration/manage_items.html', {'items': items})