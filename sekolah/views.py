import csv, io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

from .models import Student, Task


@staff_member_required()
def upload(request, action=''):
    """
    Menambahkan data dari file CSV yang diupload oleh admin. Terdapat tiga jenis
    `action` dengan format header untuk masing-masing sebagai berikut:

    `student`
        Membuat Student baru. [nim, nama depan, nama belakang]

    `assign`
        Menambahkan Student ke Task yang diberikan. [nim, nama task]

    `complete`
        Menyelesaikan Task dan memberi skor. [nim, nama task, skor]
    """
    if request.method == 'GET':
        return render(request, 'upload.html', {'action': action})

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
                user.email = f'{column[1].lower()}@skullers.com'
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

    return HttpResponseRedirect(reverse('upload'))
