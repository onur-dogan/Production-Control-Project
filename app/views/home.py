from django.shortcuts import render

def main(request):
    return render(request, 'home/index.html')