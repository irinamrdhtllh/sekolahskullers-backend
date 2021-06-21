import csv, io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RegistrationForm, LoginForm
from .models import Student


def home(request):
    return render(request, 'home.html', context=None)


def year(request):
    pass


def group(request):
    pass


def student(request):
    pass


@staff_member_required(redirect_field_name='', login_url='home')
def upload(request):
    """
    Menambahkan Student dari file CSV yang diupload
    dengan format header: `username`, `first_name`, `last_name`
    """
    if request.method == 'GET':
        return render(request, 'upload.html')

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


def register(request):
    """
    Membuat Student dengan field: username, first_name, last_name, email.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
