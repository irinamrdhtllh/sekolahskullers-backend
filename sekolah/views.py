from django.shortcuts import render


def home(request):
    return render(request, 'sekolah/home.html', context=None)


def year(request):
    pass


def group(request):
    pass


def student(request):
    pass
