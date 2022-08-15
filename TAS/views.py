import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .face_recognition_driver import get_encodings
from .forms import AddUserForm
from .models import User, Department, TimeTracking


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {}
    return render(request, 'TAS/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    if request.user.is_boss:
        department = Department.objects.get(department_head__user_id=request.user.user_id)
    else:
        department = Department.objects.get(department_head__user_id=request.user.boss.user_id)

    users = User.objects.filter(
        Q(boss__user_id__icontains=request.user.user_id))
    users_count = users.count()
    users_online_count = users.filter(Q(at_workplace=True)).count()

    users = users.filter(
        Q(full_name__icontains=q) |
        Q(pernr__icontains=q) |
        Q(position__icontains=q) |
        Q(email__icontains=q) |
        Q(user_phone_num__icontains=q))
    users.filter()
    context = {'users': users, 'users_count': users_count, 'users_online_count': users_online_count,
               'department': department}
    return render(request, 'TAS/home.html', context)


@login_required(login_url='/login')
def about(request, pk):
    user = User.objects.get(user_id=pk)
    # context = {'req_about': req_about}
    context = {'user_about': user}
    return render(request, 'TAS/about.html', context)


@login_required(login_url='/login')
def add_user(request, pk):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.boss = User.objects.get(user_id=pk)
            instance.username = instance.email
            instance.save()
            new_user = User.objects.get(email=instance.email)
            new_user.avatar_encodings = {'user_id': str(new_user.user_id),
                                         'encodings': get_encodings(new_user.avatar).tolist()}
            new_user.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'TAS/add_user.html', context)


@login_required(login_url='/login')
def user_profile(request, pk):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    user = User.objects.get(user_id=pk)
    # activities = TimeTracking.objects.get(user_id=pk)

    users = User.objects.filter(
        Q(boss__user_id__icontains=request.user.user_id))
    users_count = users.count()
    users_online_count = users.filter(Q(at_workplace=True)).count()

    users = users.filter(
        Q(full_name__icontains=q) |
        Q(pernr__icontains=q) |
        Q(position__icontains=q) |
        Q(email__icontains=q) |
        Q(user_phone_num__icontains=q))
    users.filter()
    context = {'user': user, 'users': users, 'users_count': users_count, 'users_online_count': users_online_count}

    # context = {'user': user}  # , 'activities': activities}
    return render(request, 'TAS/profile.html', context)


'''
@login_required(login_url='/login')
def update_user(request, pk):
    user = User.objects.get(user_id=pk)
    form = AddUserForm(instance=user)

    if request.user.user_id != user.boss.user_id:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # User.objects.filter(user_id=pk).update(boss=pk)
            return redirect('home')
    context = {'form': form}
    return render(request, 'TAS/add_user.html', context)
'''


@login_required(login_url='/login')
def update_user(request, pk):
    context = {}
    return render(request, 'TAS/update_user.html', context)


@login_required(login_url='/login')
def delete_user(request, pk):
    user = User.objects.get(user_id=pk)

    """if request.user.user_id != user.user_id:
        return HttpResponse('You are not allowed here')"""

    if request.method == 'POST' and request.user.user_id != user.user_id:
        user.delete()

        return redirect('home')
    return render(request, 'TAS/delete.html', {'user': user})


@login_required(login_url='/login')
def remove_user_from_department(request, pk):
    user = User.objects.get(user_id=pk)

    """if request.user.user_id != user.user_id:
        return HttpResponse('You are not allowed here')"""

    if request.method == 'POST' and request.user.user_id != user.user_id:
        # User.objects.filter(user_id=pk).update(department_name='')
        return redirect('home')
    return render(request, 'TAS/remove_department.html', {'user': user})


@login_required(login_url='/login')
def browse_users(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    users = User.objects.filter(boss__user_id__icontains=q)
    return render(request, 'base/browse_users.html', {'users': users})


@login_required(login_url='/login')
def export_users_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['user_id', 'event_type', 'event_date', 'event_time'])

    users = TimeTracking.objects.filter(user_id=pk).values_list('user_id', 'device_id', 'event_type', 'event_date',
                                                                'event_time')
    for user in users:
        writer.writerow(user)

    return response
