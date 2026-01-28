#
#
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
#
# from .models import User, Task
# from .serializers import TaskSerializer
#
#
# # ======================================================
# # ================= USER APIs (JWT ONLY) ================
# # ======================================================
#
# class UserTaskList(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         tasks = Task.objects.filter(assigned_to=request.user)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#
# class CompleteTask(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def put(self, request, id):
#         try:
#             task = Task.objects.get(id=id, assigned_to=request.user)
#         except Task.DoesNotExist:
#             return Response({"error": "Task not found"}, status=404)
#
#         if request.data.get('status') == 'completed':
#             if not request.data.get('completion_report') or not request.data.get('worked_hours'):
#                 return Response(
#                     {"error": "Completion report and worked hours are required"},
#                     status=400
#                 )
#
#             task.status = 'completed'
#             task.completion_report = request.data['completion_report']
#             task.worked_hours = request.data['worked_hours']
#             task.save()
#
#         return Response({"message": "Task completed successfully"})
#
#
# class TaskReport(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, id):
#         if request.user.role not in ['admin', 'superadmin']:
#             return Response({"error": "Unauthorized"}, status=403)
#
#         try:
#             task = Task.objects.get(id=id, status='completed')
#         except Task.DoesNotExist:
#             return Response({"error": "Report not available"}, status=404)
#
#         return Response({
#             "report": task.completion_report,
#             "hours": task.worked_hours
#         })
#
#
# # ======================================================
# # ================= AUTH UI (SESSION) ==================
# # ======================================================
#
# def login_view(request):
#     if request.method == 'POST':
#         user = authenticate(
#             request,
#             username=request.POST['username'],
#             password=request.POST['password']
#         )
#
#         if user:
#             login(request, user)
#             # if user.role == 'superadmin':
#             if request.user.role == 'superadmin':
#                 return redirect('/superadmin/')
#
#             elif request.user.is_superuser:
#                 print(request.user.is_superuser, '////////////')
#                 return redirect('/superadmin/')
#
#             elif user.role == 'admin':
#                 return redirect('/admin/')
#             elif user.role == 'user':
#                 return redirect('/user/')
#         return render(request, 'tasks/login.html', {'error': 'Invalid credentials'})
#
#     return render(request, 'tasks/login.html')
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('/login/')
#
#
# # ======================================================
# # ================= SUPERADMIN UI ======================
# # ======================================================
#
# @login_required
# def superadmin_dashboard(request):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     users = User.objects.all()
#     tasks = Task.objects.all()
#
#     return render(request, 'tasks/superadmin_dashboard.html', {
#         'users': users,
#         'tasks': tasks
#     })
#
#
# @login_required
# def create_admin(request):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     if request.method == 'POST':
#         User.objects.create_user(
#             username=request.POST['username'],
#             password=request.POST['password'],
#             role='admin'
#         )
#         return redirect('/superadmin/')
#
#     return render(request, 'tasks/create_admin.html')
#
#
# @login_required
# def create_user(request):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     if request.method == 'POST':
#         User.objects.create_user(
#             username=request.POST['username'],
#             password=request.POST['password'],
#             role='user'
#         )
#         return redirect('/superadmin/')
#
#     return render(request, 'tasks/create_user.html')
#
#
# @login_required
# def assign_user_admin(request):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     users = User.objects.filter(role='user')
#     admins = User.objects.filter(role='admin')
#
#     if request.method == 'POST':
#         user = User.objects.get(id=request.POST['user'])
#         admin = User.objects.get(id=request.POST['admin'])
#
#         user.assigned_admin = admin   # ensure field exists in User model
#         user.save()
#
#         return redirect('/superadmin/')
#
#     return render(request, 'tasks/assign_user_admin.html', {
#         'users': users,
#         'admins': admins
#     })
#
# @login_required
# def delete_user(request, id):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     user = User.objects.get(id=id)
#
#     # Prevent deleting yourself
#     if user == request.user:
#         return redirect('/superadmin/')
#
#     user.delete()
#     return redirect('/superadmin/')
# @login_required
# def delete_task(request, id):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     task = Task.objects.get(id=id)
#     task.delete()
#     return redirect('/superadmin/')
#
# @login_required
# def update_user(request, id):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     user = User.objects.get(id=id)
#
#     if request.method == 'POST':
#         user.username = request.POST['username']
#         user.role = request.POST['role']
#         user.save()
#         return redirect('/superadmin/')
#
#     return render(request, 'tasks/update_user.html', {'user': user})
#
# @login_required
# def update_task(request, id):
#     if request.user.role != 'superadmin':
#         return redirect('/login/')
#
#     task = Task.objects.get(id=id)
#
#     if request.method == 'POST':
#         task.title = request.POST['title']
#         task.status = request.POST['status']
#         task.save()
#         return redirect('/superadmin/')
#
#     return render(request, 'tasks/update_task.html', {'task': task})
#
#
#
# # ======================================================
# # ================= ADMIN UI ===========================
# # ======================================================
#
# @login_required
# def admin_dashboard(request):
#     if request.user.role != 'admin':
#         return redirect('/login/')
#
#     tasks = Task.objects.filter(assigned_to__role='user')
#     return render(request, 'tasks/admin_dashboard.html', {'tasks': tasks})
#
#
# @login_required
# def create_task(request):
#     user1=request.user.role
#     if request.user.role not in ['admin','superadmin']:
#         return redirect('/login/')
#     users = User.objects.filter(role='user')
#
#     if request.method == 'POST':
#         Task.objects.create(
#             title=request.POST['title'],
#             description=request.POST['description'],
#             assigned_to=User.objects.get(id=request.POST['user']),
#             status='pending'
#         )
#         print(f"/{user1}/","/////////////////////////////////////user1")
#         return redirect(f"/{user1}/")
#
#     return render(request, 'tasks/create_task.html', {'users': users})
#
#
# @login_required
# def view_tasks(request):
#     if request.user.role != 'admin':
#         return redirect('/login/')
#
#     tasks = Task.objects.filter(assigned_to__role='user')
#     return render(request, 'tasks/view_tasks.html', {'tasks': tasks})
#
#
# @login_required
# def view_reports(request):
#     if request.user.role not in ['admin', 'superadmin']:
#         return redirect('/login/')
#
#     tasks = Task.objects.filter(status='completed')
#     return render(request, 'tasks/view_reports.html', {'tasks': tasks})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Task
from .serializers import TaskSerializer


# ======================================================
# ================= USER APIs (JWT ONLY) ================
# ======================================================

class UserTaskList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.filter(assigned_to=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({"error": "Unable to fetch tasks"}, status=500)


class CompleteTask(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            task = Task.objects.get(id=id, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        except Exception:
            return Response({"error": "Something went wrong"}, status=500)

        if request.data.get('status') == 'completed':
            if not request.data.get('completion_report') or not request.data.get('worked_hours'):
                return Response(
                    {"error": "Completion report and worked hours are required"},
                    status=400
                )

            try:
                task.status = 'completed'
                task.completion_report = request.data['completion_report']
                task.worked_hours = request.data['worked_hours']
                task.save()
            except Exception:
                return Response({"error": "Failed to update task"}, status=500)

        return Response({"message": "Task completed successfully"})


class TaskReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.role not in ['admin', 'superadmin']:
            return Response({"error": "Unauthorized"}, status=403)

        try:
            task = Task.objects.get(id=id, status='completed')
            return Response({
                "report": task.completion_report,
                "hours": task.worked_hours
            })
        except Task.DoesNotExist:
            return Response({"error": "Report not available"}, status=404)
        except Exception:
            return Response({"error": "Something went wrong"}, status=500)


# ======================================================
# ================= AUTH UI (SESSION) ==================
# ======================================================

def login_view(request):
    if request.method == 'POST':
        try:
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )
        except Exception:
            return render(request, 'tasks/login.html', {'error': 'Authentication failed'})

        if user:
            login(request, user)

            if request.user.role == 'superadmin':
                return redirect('/superadmin/')
            elif request.user.is_superuser:
                return redirect('/superadmin/')
            elif user.role == 'admin':
                return redirect('/admin/')
            elif user.role == 'user':
                return redirect('/user/')

        return render(request, 'tasks/login.html', {'error': 'Invalid credentials'})

    return render(request, 'tasks/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


# ======================================================
# ================= SUPERADMIN UI ======================
# ======================================================

@login_required
def superadmin_dashboard(request):
    if request.user.role != 'superadmin':
        return redirect('/login/')

    try:
        users = User.objects.all()
        tasks = Task.objects.all()
    except Exception:
        return redirect('/login/')

    return render(request, 'tasks/superadmin_dashboard.html', {
        'users': users,
        'tasks': tasks
    })


@login_required
def create_admin(request):
    if request.user.role != 'superadmin':
        return redirect('/login/')

    if request.method == 'POST':
        try:
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                role='admin'
            )
            return redirect('/superadmin/')
        except Exception:
            return render(request, 'tasks/create_admin.html', {'error': 'Failed to create admin'})

    return render(request, 'tasks/create_admin.html')


@login_required
def create_user(request):
    if request.user.role != 'superadmin':
        return redirect('/login/')

    if request.method == 'POST':
        try:
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                role='user'
            )
            return redirect('/superadmin/')
        except Exception:
            return render(request, 'tasks/create_user.html', {'error': 'Failed to create user'})

    return render(request, 'tasks/create_user.html')


@login_required
def assign_user_admin(request):
    if request.user.role != 'superadmin':
        return redirect('/login/')

    users = User.objects.filter(role='user')
    admins = User.objects.filter(role='admin')

    if request.method == 'POST':
        try:
            user = User.objects.get(id=request.POST['user'])
            admin = User.objects.get(id=request.POST['admin'])
            user.assigned_admin = admin
            user.save()
            return redirect('/superadmin/')
        except Exception:
            return render(request, 'tasks/assign_user_admin.html', {
                'users': users,
                'admins': admins,
                'error': 'Assignment failed'
            })

    return render(request, 'tasks/assign_user_admin.html', {
        'users': users,
        'admins': admins
    })


@login_required
def delete_user(request, id):
    if request.user.role != 'superadmin':
        return redirect('/login/')

    try:
        user = User.objects.get(id=id)
        if user != request.user:
            user.delete()
    except Exception:
        pass

    return redirect('/superadmin/')


@login_required
def delete_task(request, id):
    if request.user.role not in ['superadmin','admin']:
        return redirect('/login/')

    try:
        task = Task.objects.get(id=id)
        task.delete()
    except Exception:
        pass

    return redirect(f'/{request.user.role}/')


@login_required
def update_user(request, id):
    if request.user.role != 'superadmin':
        return redirect('/login/')

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect('/superadmin/')

    if request.method == 'POST':
        try:
            user.username = request.POST['username']
            user.role = request.POST['role']
            user.save()
            return redirect('/superadmin/')
        except Exception:
            return render(request, 'tasks/update_user.html', {'user': user, 'error': 'Update failed'})

    return render(request, 'tasks/update_user.html', {'user': user})


@login_required
def update_task(request, id):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('/login/')

    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return redirect(f'/{request.user.role}/')

    if request.method == 'POST':
        status = request.POST.get('status')

        # 🔴 If marking as completed, report & hours are mandatory
        if status == 'completed':
            completion_report = request.POST.get('completion_report')
            worked_hours = request.POST.get('worked_hours')

            if not completion_report or not worked_hours:
                return render(
                    request,
                    'tasks/update_task.html',
                    {
                        'task': task,
                        'error': 'Completion report and worked hours are required when completing a task'
                    }
                )

            task.completion_report = completion_report
            task.worked_hours = worked_hours

        try:
            task.title = request.POST.get('title')
            task.status = status
            task.save()
            return redirect(f'/{request.user.role}/')
        except Exception:
            return render(
                request,
                'tasks/update_task.html',
                {'task': task, 'error': 'Update failed'}
            )

    return render(request, 'tasks/update_task.html', {'task': task})



# @login_required
# def update_task(request, id):
#     if request.user.role not in ['admin','superadmin']:
#         return redirect('/login/')
#
#     try:
#         task = Task.objects.get(id=id)
#     except Task.DoesNotExist:
#         return redirect(f'/{request.user.role}/')
#
#     if request.method == 'POST':
#         try:
#             task.title = request.POST['title']
#             task.status = request.POST['status']
#             task.save()
#             return redirect(f'/{request.user.role}/')
#         except Exception:
#             return render(request, 'tasks/update_task.html', {'task': task, 'error': 'Update failed'})
#
#     return render(request, 'tasks/update_task.html', {'task': task})




# ======================================================
# ================= ADMIN UI ===========================
# ======================================================

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('/login/')

    try:
        tasks = Task.objects.filter(assigned_to__role='user')
    except Exception:
        tasks = []

    return render(request, 'tasks/admin_dashboard.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('/login/')

    users = User.objects.filter(role='user')

    if request.method == 'POST':
        try:
            Task.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                assigned_to=User.objects.get(id=request.POST['user']),
                status='pending'
            )
            return redirect(f"/{request.user.role}/")
        except Exception:
            return render(request, 'tasks/create_task.html', {'users': users, 'error': 'Task creation failed'})

    return render(request, 'tasks/create_task.html', {'users': users})


@login_required
def view_tasks(request):
    if request.user.role != 'admin':
        return redirect('/login/')

    try:
        tasks = Task.objects.filter(assigned_to__role='user')
    except Exception:
        tasks = []

    return render(request, 'tasks/view_tasks.html', {'tasks': tasks})


@login_required
def view_reports(request):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('/login/')

    try:
        tasks = Task.objects.filter(status='completed')
    except Exception:
        tasks = []

    return render(request, 'tasks/view_reports.html', {'tasks': tasks})

