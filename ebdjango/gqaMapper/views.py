from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'gqaMapper/index.html')

def search(request):
    return render(request, 'gqaMapper/search.html')

def help(request):
    return render(request, 'gqaMapper/help.html')