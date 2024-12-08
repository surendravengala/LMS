from django.contrib import admin
from .models import Student, Teacher,CourseVideo,Assignment,Submission

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(CourseVideo)
admin.site.register(Assignment)
admin.site.register(Submission)