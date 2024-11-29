from django.shortcuts import render

def ratings(request):
    return render(request, 'ratings/index.html')
