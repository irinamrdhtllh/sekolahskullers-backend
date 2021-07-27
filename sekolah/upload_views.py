import csv
import io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Group, Student


@staff_member_required()
def upload(request, action=''):
    """
    Menambahkan data dari file CSV yang diupload oleh admin. Terdapat tiga jenis
    `action` dengan format header untuk masing-masing sebagai berikut:

    `student`
        Membuat Student baru (hanya untuk percobaan). [nim, nama depan, nama belakang]

    `group`
        Menambahkan Student ke Group. [nim, nama group]

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

        elif action == 'group':
            group, _ = Group.objects.get_or_create(name=column[1])
            user = get_object_or_404(User, username=column[0])
            user.student.group = group
            user.student.save()

        elif action == 'complete':
            user = get_object_or_404(User, username=column[0])
            user.student.complete_task(column[1], column[2])

        elif action == 'health':
            user = get_object_or_404(User, username=column[0])
            user.student.health = column[1]
            user.student.save()

        elif action == 'assessment':
            user = get_object_or_404(User, username=column[0])
            user.student.assessment.assessment1 = column[1]
            user.student.assessment.assessment2 = column[2]
            user.student.assessment.assessment3 = column[3]
            user.student.assessment.assessment4 = column[4]
            user.student.assessment.assessment5 = column[5]
            user.student.assessment.assessment6 = column[6]
            user.student.assessment.assessment7 = column[7]
            user.student.assessment.save()

    return HttpResponseRedirect(reverse('upload'))
