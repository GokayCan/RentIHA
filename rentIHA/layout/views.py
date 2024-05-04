from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
@login_required
def home(request):
    return render(request, 'index.html')