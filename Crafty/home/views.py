from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home/index.html')  # Render the homepage

def about(request):
    return render(request, 'home/about.html')  # Render the about page
