import csv, io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets, permissions

from .forms import RegistrationForm
from .models import Student, Task
from .serializers import StudentSerializer


def home(request):
    return render(request, 'home.html', {'user': request.user})


def year(request):
    pass


def group(request):
    pass


def student(request):
    students = Student.objects.all()
    return render(request, 'student.html', {'students': students})


@staff_member_required(login_url='login')
def upload(request, action):
    """
    Menambahkan data dari file CSV yang diupload oleh admin. Terdapat tiga jenis
    aksi dengan format header masing-masing sebagai berikut:
    1. student (membuat Student baru): nim, nama depan, nama belakang
    2. assign (menambahkan Student ke Task yang diberikan): nim, nama task
    3. complete (menyelesaikan Task dan memberi skor): nim, nama task, skor
    """
    if request.method == 'GET':
        return render(request, 'upload.html')

    file = request.FILES['file']
    data = file.read().decode('UTF-8')
    io_string = io.StringIO(data)
    next(io_string)

    for column in csv.reader(io_string):
        if action == 'student':
            user, created = User.objects.get_or_create(
                username=column[0], first_name=column[1], last_name=column[2]
            )
            if created:
                Student.objects.create(user=user)

        elif action == 'assign':
            user = get_object_or_404(User, username=column[0])
            task = get_object_or_404(Task, name=column[1])
            task.assign(user.student)

        elif action == 'complete':
            user = get_object_or_404(User, username=column[0])
            user.student.complete_task(column[1], column[2])

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
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'student': request.user.student})
    else:
        return HttpResponseRedirect(reverse('login'))


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user__username'
