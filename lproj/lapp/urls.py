from django.urls import path
from . import views

urlpatterns = [
    path('s_reg/', views.student_form, name='student_form'),
    path('s_login/', views.student_login, name='student_login'),
    path('t_login/', views.login_teacher, name='login_teacher'),
    path('s_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('t_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('create_assignment/', views.create_assignment,name='create_assignment'),
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('view_submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    path('success/', views.success_view, name='success_url'),
    path('logout/', views.logout, name='logout'),
]