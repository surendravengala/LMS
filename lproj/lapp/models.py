from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Student(models.Model):
    userid = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)  # Increased length for hashed passwords
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()  # Use BigIntegerField for phone numbers
    mail = models.EmailField()
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
    )
    course = models.CharField(
        max_length=50,
        choices=[('Python', 'Python'), ('Java', 'Java'), ('CoreJava', 'Core Java')],
    )


class Course(models.Model):
    name = models.CharField(max_length=100)  # Course name
    description = models.TextField()  # A brief description of the course
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='assigned_courses')
    def __str__(self):
        return self.name


class Teacher(models.Model):
    userid = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)  # length of plain passwords
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()  # Use BigIntegerField for phone numbers
    mail = models.EmailField()
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
    )
    courses = models.ManyToManyField(Course,related_name="teachers",blank=True)

    

class CourseVideo(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.CharField(
        max_length=50,
        choices=[('Python', 'Python'), ('Java', 'Java'), ('CoreJava', 'Core Java')],
    )
    video = models.CharField(max_length=10000)
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.CharField(
        max_length=50,
        choices=[('Python', 'Python'), ('Java', 'Java'), ('CoreJava', 'Core Java')],
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, related_name='assignments',blank=True)



    submissions = models.ManyToManyField(
        Student,
        through='Submission',
        related_name='assignment_submissions'
    )

    def __str__(self):
        return self.title

    

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    link =models.CharField(max_length=500 ,null=True,blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"




