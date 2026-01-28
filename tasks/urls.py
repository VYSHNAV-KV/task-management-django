from django.urls import path
from .views import (
    # API views
    # UserTaskList,
    # CompleteTask,
    # TaskReport,

    # Auth UI
    login_view,
    logout_view,

    # SuperAdmin UI
    superadmin_dashboard,
    create_admin,
    create_user,
    assign_user_admin,
    delete_task,
    delete_user,
    update_user,
    update_task,

    # Admin UI
    admin_dashboard,
    create_task,
    view_tasks,
    view_reports,
    user_tasks,
    complete_task,
    task_report


)

urlpatterns = [

    # ================= API (JWT) =================
    
    path("tasks/", user_tasks),
    path("tasks/<int:id>/", complete_task),
    path("tasks/<int:id>/report/", task_report),

    # path('tasks/', UserTaskList.as_view(), name='user_tasks'),
    # path('tasks/<int:id>/', CompleteTask.as_view(), name='complete_task'),
    # path('tasks/<int:id>/report/', TaskReport.as_view(), name='task_report'),

    # ================= AUTH UI ===================
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # ================= SUPERADMIN UI ==============
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/create-admin/', create_admin, name='create_admin'),
    path('superadmin/create-user/', create_user, name='create_user'),
    path('superadmin/assign/', assign_user_admin, name='assign_user_admin'),

    path('superadmin/user/delete/<int:id>/', delete_user, name='delete_user'),
    path('superadmin/task/delete/<int:id>/', delete_task, name='delete_task'),
    path('superadmin/user/update/<int:id>/', update_user, name='update_user'),
    path('superadmin/task/update/<int:id>/', update_task, name='update_task'),


    # ================= ADMIN UI ===================
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin/create-task/', create_task, name='create_task'),
    path('admin/tasks/', view_tasks, name='view_tasks'),

    # ================= REPORTS ====================
    path('reports/', view_reports, name='view_reports'),
]
