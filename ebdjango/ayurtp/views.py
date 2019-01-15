from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': "Ayurvedic-Therapeutics | Home",
    }
    return render(request, 'ayurtp/index.html', context)

def search(request):
    context = {
        'title': "Ayurvedic-Therapeutics | Search",
    }
    return render(request, 'ayurtp/search.html', context)

def download(request):
    context = {
        'title': "Ayurvedic-Therapeutics | Download",
    }
    return render(request, 'ayurtp/download.html', context)

def statistics(request):
    context = {
        'title': "Ayurvedic-Therapeutics | Statistics",
    }
    return render(request, 'ayurtp/statistics.html', context)

def help(request):
    context = {
        'title': "Ayurvedic-Therapeutics | Help",
    }
    return render(request, 'ayurtp/help.html', context)
