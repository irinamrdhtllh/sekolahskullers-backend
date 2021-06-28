import csv, io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

from .models import Student, Task


def home(request):
    return render(request, 'home.html')


@staff_member_required()
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
            user, created = User.objects.get_or_create(username=column[0])
            if created:
                user.first_name = column[1]
                user.last_name = column[2]
                user.email = f'{column[1]}@skullers.com'
                user.set_password(column[0])
                user.save()
                Student.objects.create(user=user)

        elif action == 'assign':
            user = get_object_or_404(User, username=column[0])
            task = get_object_or_404(Task, name=column[1])
            task.assign(user.student)

        elif action == 'complete':
            user = get_object_or_404(User, username=column[0])
            user.student.complete_task(column[1], column[2])

    return HttpResponseRedirect(reverse('home'))
