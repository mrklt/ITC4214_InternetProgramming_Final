from django.shortcuts import render

def products(request):
    return render(request, 'products/index.html')  # Adjust the template as needed
