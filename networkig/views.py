from django.shortcuts import render

# Create your views here.
def network(request):
    return render(request,'networking/Home_network.html')