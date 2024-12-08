from django import forms
from .models import Student, Teacher, CourseVideo,Assignment,Submission
from django.contrib.auth.hashers import make_password


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['userid','password', 'name', 'phone', 'mail', 'gender', 'course']
        widgets = {
            'password': forms.PasswordInput(),  # Hide password input
        }

    def save(self, commit=True):
        student = super().save(commit=False)

        if commit:
            student.save()
        return student




class TeacherLoginForm(forms.Form):
    userid = forms.CharField(max_length=10, label="User ID")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ['course', 'video', 'title']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date']





class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['link']
