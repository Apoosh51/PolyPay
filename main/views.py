from django.shortcuts import render

def home(request):
    return render(request, 'main/index.html')

def shop(request):
    return render(request, 'main/shop.html')

def about_bank(request):
    return render(request, 'main/about_bank.html')

def deposits(request):
    return render(request, 'main/deposits.html')
