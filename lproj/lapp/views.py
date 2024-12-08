from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseRedirect
from .forms import StudentForm,TeacherLoginForm,VideoUploadForm,AssignmentForm,SubmissionForm
from .models import Teacher,Student,CourseVideo,Assignment,Submission
from django.contrib.auth.hashers import check_password
from django.db.models import Prefetch
from collections import defaultdict
from django.urls import reverse
from django.contrib import messages
def student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your form has been successfully submitted!')
            return redirect(reverse('success_url'))  # Redirect using the named URL pattern
    else:
        form = StudentForm()
    return render(request, 'lapp/student_form.html', {'form': form})



def success_view(request):
    return render(request, 'lapp/success.html')


def login_teacher(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']

            try:
                teacher = Teacher.objects.get(userid=userid)
                # Compare plain-text password
                if teacher.password == password:  # If password matches
                    request.session.flush() 
                    request.session['teacher_id'] = teacher.id  # Store teacher ID in session
                    return redirect('teacher_dashboard')  # Redirect to the dashboard
                else:
                    return render(request, 'lapp/teacher_login.html', {
                        'form': form,
                        'error': 'Invalid Password',
                    })
            except Teacher.DoesNotExist:
                return render(request, 'lapp/teacher_login.html', {
                    'form': form,
                    'error': 'Invalid UserID',
                })

    else:
        form = TeacherLoginForm()
    return render(request, 'lapp/teacher_login.html', {'form': form})



def upload_video(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('login_teacher')  # Redirect if not logged in



    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.teacher_id = teacher_id  # Assign the logged-in teacher to the video
            video.save()
            return redirect('teacher_dashboard')  # Redirect after successful upload
    else:
        form = VideoUploadForm()
    return render(request, 'lapp/upload_video.html', {'form': form})



def student_login(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(userid=userid)
            if student.password == password:  # Simple password check (consider using hashed passwords)
                request.session.flush()  # Clear all session data
                request.session['student_id'] = student.id
                request.session['student_course'] = student.course
                return redirect('student_dashboard')
            else:
                return render(request, 'lapp/student_login.html', {'error': 'Invalid Password'})
        except Student.DoesNotExist:
            return render(request, 'lapp/student_login.html', {'error': 'Invalid UserID'})

    return render(request, 'lapp/student_login.html')


# Student Dashboard View
def student_dashboard(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_login')  # Redirect if not logged in
    
    student_course = request.session.get('student_course')
    student = Student.objects.get(id=student_id)
    
    # Fetch videos and assignments based on the student's course
    course_videos = CourseVideo.objects.filter(course=student_course)
    assignments = Assignment.objects.filter(course=student_course)

    # Annotate assignments with submission status for the logged-in student
    assignment_data = []
    for assignment in assignments:
        submission = Submission.objects.filter(student=student, assignment=assignment).first()
        assignment_data.append({
            'assignment': assignment,
            'submission': submission,
        })
    
    # Debugging: Print assignment IDs
    print("Assignments:", [data['assignment'].id for data in assignment_data])
    
    return render(request, 'lapp/student_dashboard.html', {
        'student_name': student.name,
        'course': student_course,
        'videos': course_videos,
        'assignments': assignment_data,
    })



# Teacher Dashboard View

def teacher_dashboard(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('login_teacher')  # Redirect if not logged in

    teacher = Teacher.objects.get(id=teacher_id)
    assignments = Assignment.objects.filter(teacher=teacher).prefetch_related('submissions')

     # Group assignments by course
    assignments_by_course = defaultdict(list)
    for assignment in assignments:
        assignments_by_course[assignment.course].append(assignment)

    

    # Fetch videos and assignments for the teacher's course
    course_videos = CourseVideo.objects.filter(teacher_id=teacher_id)
    courses = teacher.courses.all()

    # Handle form submission to create assignments or upload videos
    if request.method == 'POST':
        if 'upload_video' in request.POST:
            return redirect('upload_video')
        elif 'create_assignment' in request.POST:
            return redirect('create_assignment')  # Redirect to assignment creation view

    return render(request, 'lapp/teacher_dashboard.html', {
        'teacher_name': teacher.name,
        'course_videos': course_videos,
        'assignments': assignments,
        'assignments_by_course': dict(assignments_by_course),
        'courses': courses,
    })




# Assignment Creation View
def create_assignment(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('login_teacher')  # Redirect if not logged in

    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher  # Assign the teacher to the assignment
            assignment.save()
            return redirect('teacher_dashboard')  # Redirect after successful creation
    else:
        form = AssignmentForm()

    return render(request, 'lapp/create_assignment.html', {'form': form})


def logout(request):
    if 'teacher_id' in request.session:
        # Clear session for teacher
        request.session.flush()
        return redirect('login_teacher')  # Redirect to teacher login page
    elif 'student_id' in request.session:
        # Clear session for student
        request.session.flush()
        return redirect('student_login')  # Redirect to student login page
    else:
        # Default redirection if no specific session found
        return redirect('student_login')  # Fallback to student login






def submit_assignment(request, assignment_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')  # Redirect if not logged in

    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = get_object_or_404(Student,id=student_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.assignment = assignment
            submission.save()
            return redirect('student_dashboard')  # Redirect after successful submission
    else:
        form = SubmissionForm()

    return render(request, 'lapp/submit_assignment.html', {
        'form': form,
        'assignment': assignment
    })

def submissions(self):
    return Submission.objects.filter(assignment=self)

def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'lapp/view_submissions.html', {'assignment': assignment})