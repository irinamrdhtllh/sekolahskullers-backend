import csv, io

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Student


def home(request):
    return render(request, 'sekolah/home.html', context=None)


def year(request):
    pass


def group(request):
    pass


def student(request):
    pass


def upload(request):
    """
    Menambahkan Student dari file CSV yang diupload 
    dengan format header: `username`, `first_name`, `last_name`
    """
    if request.method == 'GET':
        return render(request, 'sekolah/upload.html')

    file = request.FILES['file']
    data = file.read().decode('UTF-8')
    io_string = io.StringIO(data)
    next(io_string)

    for column in csv.reader(io_string):
        user, created = User.objects.get_or_create(
            username=column[0], first_name=column[1], last_name=column[2]
        )
        if created:
            Student.objects.create(user=user)

    return HttpResponseRedirect(reverse('home'))
