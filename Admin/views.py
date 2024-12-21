from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from pyexpat.errors import messages
from .models import *
from django.contrib.auth import logout

from django.db.models import Sum


def home(request):
    if 'uname' in request.session:
        fee_collected = StudentFeesStatus.objects.filter(status='Paid').aggregate(total_collected=Sum('amount_paid'))[
                            'total_collected'] or 0
        outstanding_fees = StudentFeesStatus.objects.filter(status='Due').aggregate(total_due=Sum('amount_paid'))[
                               'total_due'] or 0
        recent_payments = StudentFeesStatus.objects.filter(status='Paid').order_by('paid_date')[:5]
        payment_dues = StudentFeesStatus.objects.filter(status='Due')
        context = {
            'fee_collected': fee_collected,
            'outstanding_fees': outstanding_fees,
            'recent_payments': recent_payments,
            'payment_dues': payment_dues
        }
        return render(request, 'adminhome.html', context)

    return redirect('login')


def student_panel(request):
    data = Students.objects.all()
    return render(request, template_name='studenthome.html', context={'data': data})


# def fee_panel(request):
#     fee_categories = FeeCategories.objects.all()
#     return render(request, 'feepanel.html', {'fee_categories': fee_categories})
#

def add_student(request):
    if request.method == "POST":
        student_obj = Students()
        student_obj.first_name = request.POST.get('firstname')
        student_obj.last_name = request.POST.get('lastname')
        student_obj.class_name = request.POST.get('classname')
        student_obj.roll_number = request.POST.get('rollno')
        student_obj.email_id = request.POST.get('email')
        student_obj.save()
        return redirect('/student_panel/')
    return render(request, 'addstudent.html')


def fee_payments(request, student_id):
    student = Students.objects.get(id=student_id)
    student_fees = StudentFeesStatus.objects.filter(student=student)

    if request.method == 'POST':
        fee_id = request.POST['fee_category']
        status = request.POST['status']
        amount_paid = request.POST['amount_paid']
        paid_date = request.POST.get('paid_date', None)

        fee_category = FeeCategories.objects.get(id=fee_id)
        fee = StudentFeesStatus.objects.get(student=student, fee_category=fee_category)
        fee.status = status
        fee.amount_paid = amount_paid
        if status == 'Paid':
            fee.paid_date = paid_date
        fee.save()
        messages.success(request, "Payment status updated successfully.")
        return redirect('manage_payments', student_id=student.id)

    fee_categories = FeeCategories.objects.all()
    return render(request, 'feepayment.html',
                  {'student': student, 'fee_categories': fee_categories, 'student_fees': student_fees})


def delete_student(request, id):
    student_obj = Students.objects.get(id=id)
    student_obj.delete()
    return redirect('/student_panel')


def edit_student(request, id):
    student_obj = Students.objects.get(id=id)
    print("student_obj")
    if request.method == "POST":
        student_obj = Students.objects.get(id=id)

        student_obj.first_name = request.POST.get('firstname')
        student_obj.last_name = request.POST.get('lastname')
        student_obj.class_name = request.POST.get('classname')
        student_obj.roll_number = request.POST.get('rollno')
        student_obj.email_id = request.POST.get('email')
        student_obj.save()
        return redirect('home/')
    return render(request, 'editstudent.html', {'data': student_obj})


def login(request):
    if request.method == "POST":
        user_name = request.POST.get('uname')
        password = request.POST.get('upass')
        user = Roles.objects.filter(user_name=user_name).first()

        if user and check_password(password, user.password):
            request.session['uname'] = user_name
            return redirect('/home/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        user_obj = Roles()

        user_obj.user_name = request.POST.get('uname')
        user_obj.password = request.POST.get('upass')
        user_obj.save()
        return redirect('/login/')
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def student_fee_status_view(request):
    students = Students.objects.all()
    fee_statuses = StudentFeesStatus.objects.all()
    context = {
        'students': students,
        'fee_statuses': fee_statuses,
    }
    return render(request, 'student_fee_status.html', context)


def add_edit_fee_detail_view(request, fee_status_id=None):
    if fee_status_id:
        fee_status = get_object_or_404(StudentFeesStatus, id=fee_status_id)
    else:
        fee_status = None

    if request.method == 'POST':
        student_id = request.POST['student']
        fee_category_id = request.POST['fee_category']
        status = request.POST['status']
        due_date = request.POST['due_date']
        paid_date = request.POST['paid_date']
        amount_paid = request.POST['amount_paid']

        student = get_object_or_404(Students, id=student_id)
        fee_category = get_object_or_404(FeeCategories, id=fee_category_id)

        if fee_status:
            fee_status.student = student
            fee_status.fee_category = fee_category
            fee_status.status = status
            fee_status.due_date = due_date
            fee_status.paid_date = paid_date
            fee_status.amount_paid = amount_paid
            fee_status.save()
        else:
            StudentFeesStatus.objects.create(
                student=student,
                fee_category=fee_category,
                status=status,
                due_date=due_date,
                paid_date=paid_date,
                amount_paid=amount_paid
            )

        return redirect('student_fee_status')

    students = Students.objects.all()
    fee_categories = FeeCategories.objects.all()
    return render(request, 'add_edit_fee_detail.html',
                  {'students': students, 'fee_categories': fee_categories, 'fee_status': fee_status})
