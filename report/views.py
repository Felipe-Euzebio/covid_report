from django.shortcuts import render

# Create your views here.


def show_report(request):
    return render(request, 'report.html')
