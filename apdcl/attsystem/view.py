# from openpyxl import Workbook
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser,attendance,holiday_list

# Create your views here.

# Registration view
def registration(request):
    boss=CustomUser.objects.filter(is_boss=True)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # office = request.POST.get('office')
        joining_date = request.POST.get('joining_date')
        # designation = request.POST.get('designation')
        # department = request.POST.get('department')
        boss_name = request.POST.get('bossName')
        # is_boss = request.POST.get('is_boss')
       
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('registration')
        else:
            if password == password2:
                
                user = CustomUser.objects.create_user(username=username, password=password, firstname=firstname, lastname=lastname, email=email, phone=phone, joining_date=joining_date, boss_name=boss_name)
                user.set_password(password)
                user.request_date = datetime.now().date()
                user.save()
                messages.success(request, 'User Created Successfully!')
                return redirect('log_in')
            else:
                messages.error(request, 'Passwords do not match!')
                return redirect('registration')
    
    return render(request, 'registration.html',{'boss':boss})

# Log in view
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_boss:
                login(request, user)
                return redirect('profile')
            else:
                login(request, user)
                return redirect('subordinate_profile')
            # return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect!')
            return redirect('log_in')
    return render(request, 'log_in.html')

# Home view
@login_required(login_url='log_in')
def home(request):
    current_date = datetime.now().date()
    logged_in_user = request.user
    username = CustomUser.objects.get(username=logged_in_user.username)
    total_days = (current_date - username.joining_date).days
    holidays = holiday_list.objects.filter(date__range=[username.joining_date, current_date])
    holidays_count = holidays.count()
    total_working_days = total_days - holidays_count
    total_present = attendance.objects.filter(username=username, status='Present').count()
    present_percentage = (total_present / total_working_days) * 100
    user=username
    attendance_record = attendance.objects.filter(username=user, date=datetime.now().date())
    attendance_exist = attendance_record.exists()

    accounts_count=CustomUser.objects.filter(boss_name=logged_in_user.username,is_response=False,is_staff=False)

    logged_in_user = request.user
    account_count=CustomUser.objects.filter(boss_name=logged_in_user.username)
    user_email=account_count.values_list('email')
    attendance_request_count = attendance.objects.filter(username__email__in=user_email, is_respond=False)

    return render(request, 'home.html',{'logged_in_user':logged_in_user, 'attendance_record':attendance_record, 'attendance_exist':attendance_exist,'present_percentage':present_percentage,'total_present':total_present,'accounts_count':accounts_count,'attendance_request_count':attendance_request_count})

# Profile view
def profile(request):
    return render(request, 'profile.html')

# Edit Profile View
@login_required(login_url='log_in')
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        user.designation = request.POST.get('designation')
        user.department = request.POST.get('department')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.gender = request.POST.get('gender')
        user.office = request.POST.get('office')
        user.joining_date = request.POST.get('joining_date')
        user.address = request.POST.get('address')
        user.phone = request.POST.get('phone')
        user.email = request.POST.get('email')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile_edit.html', {'user': user})

#Logout view
@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')

# Account request view
@login_required(login_url='log_in')
def accrequest(request):
    logged_in_user = request.user
    accounts=CustomUser.objects.filter(boss_name=logged_in_user.username)
    # accounts=CustomUser.objects.filter(is_active=False ,is_response=False,boss_name=logged_in_user.username)
    return render(request, 'accrequest.html',{'accounts':accounts})

# Attendance request view
@login_required(login_url='log_in')
def attrequest(request):
    logged_in_user = request.user
    accounts = CustomUser.objects.filter(boss_name=logged_in_user.username)
    user_email = accounts.values_list('email')
    search_query = request.GET.get('search', '')

    # Filter attendance records based on search query
    attendance_record = attendance.objects.filter(username__email__in=user_email)
    if search_query:
        attendance_record = attendance_record.filter(
            username__firstname__icontains=search_query) | attendance_record.filter(
            username__lastname__icontains=search_query) | attendance_record.filter(
            username__username__icontains=search_query)

    return render(request, 'attrequest.html', {
        'attendance_record': attendance_record,
        'accounts': accounts,
        'logged_in_user': logged_in_user,
        'user_email': user_email,
        'search_query': search_query  # Pass search query to template to retain search input
    })
# Dashboard view
@login_required(login_url='log_in')
# def dashboard(request):
#     logged_in_user = request.user
#     accounts_count=CustomUser.objects.filter(is_response=True,is_staff=True,boss_name=logged_in_user.username)
#     accounts=CustomUser.objects.filter(boss_name=logged_in_user.username)
#     user_email=accounts.values_list('email')
#     attendance_record = attendance.objects.filter(username__email__in=user_email)
#     return render(request, 'dashboard.html', {'attendance_record':attendance_record,'accounts':accounts,'logged_in_user':logged_in_user,'user_email':user_email,'accounts_count':accounts_count})
def dashboard(request):
    logged_in_user = request.user
    accounts_count = CustomUser.objects.filter(is_response=True, is_staff=True, boss_name=logged_in_user.username)
    accounts = CustomUser.objects.filter(boss_name=logged_in_user.username)
    user_email = accounts.values_list('email')
    
    # Determine filter type (default to 'today' if not specified)
    filter_type = request.GET.get('filter', 'today')
    search_query = request.GET.get('search', '')

    # Define date ranges based on filter type
    if filter_type == 'today':
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
    elif filter_type == '7d':
        start_date = datetime.now().date() - timedelta(days=7)
        end_date = datetime.now().date() + timedelta(days=1)
    elif filter_type == '30d':
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date() + timedelta(days=1)
    elif filter_type == '6m':
        start_date = datetime.now().date() - timedelta(days=30 * 6)
        end_date = datetime.now().date() + timedelta(days=1)
    elif filter_type == '1y':
        start_date = datetime.now().date() - timedelta(days=365)
        end_date = datetime.now().date() + timedelta(days=1)
    else:
        # Default to 'today' filter if invalid filter type
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)

    # Filter attendance records based on date range and search query
    attendance_record = attendance.objects.filter(
        username__email__in=user_email,
        date__range=[start_date, end_date]
    )

    if search_query:
        attendance_record = attendance_record.filter(
            username__firstname__icontains=search_query) | attendance_record.filter(
            username__lastname__icontains=search_query) | attendance_record.filter(
            username__username__icontains=search_query)

    return render(request, 'dashboard.html', {
        'attendance_record': attendance_record,
        'accounts': accounts,
        'logged_in_user': logged_in_user,
        'user_email': user_email,
        'accounts_count': accounts_count,
        'filter_type': filter_type,  # Optional: Pass filter type to template for highlighting active filter
        'search_query': search_query  # Pass search query to template to retain search input
    })
# My employee view  
@login_required(login_url='log_in')
def myemployee(request):
    logged_in_user = request.user
    search_query = request.GET.get('search', '')

    # Filter accounts based on search query
    accounts = CustomUser.objects.filter(is_response=True, is_staff=True, boss_name=logged_in_user.username)
    if search_query:
        accounts = accounts.filter(
            firstname__icontains=search_query) | accounts.filter(
            lastname__icontains=search_query) | accounts.filter(
            username__icontains=search_query) | accounts.filter(
            designation__icontains=search_query) | accounts.filter(
            department__icontains=search_query)

    return render(request, 'myemployee.html', {'accounts': accounts, 'search_query': search_query})

#view details view
def view_details(request, id, from_page):
    employee = CustomUser.objects.get(id=id)
    return render(request, 'view_details.html',{'employee':employee, 'from_page':from_page})

#Account request view
@login_required(login_url='log_in')
def request_response(request, username, action):
    employee = CustomUser.objects.get(username=username)
    
    if action == 'accept':
        employee.is_staff = True
        employee.is_active = True
        employee.is_response = True
        employee.request_response_date = datetime.now().date()
        employee.save()
        return redirect('/accrequest')
    elif action == 'reject':
        employee.is_active = False
        employee.is_response = True
        employee.request_response_date = datetime.now().date()
        employee.save()
        return redirect('/accrequest')
    return render(request, 'view_details.html',{'employee':employee})
@login_required(login_url='log_in')
def edit_active_status(request, username):
    employee = CustomUser.objects.get(username=username)
    if employee.is_active:
        employee.is_active = False
    else:
        employee.is_active = True
    employee.save()
    return redirect('/myemployee')

#Attendance view
@login_required(login_url='log_in')
def attendance_submit(request, username, action):
    user= CustomUser.objects.get(username=username)
    user=user
    if holiday_list.objects.filter(date=datetime.now().date()).exists():
        messages.error(request, 'Today is a holiday!')
        return redirect('/home')
    else:   
        attendance_record = attendance.objects.filter(username=user, date=datetime.now().date())
        username = CustomUser.objects.get(username=username)
        if attendance_record.count() > 0:
            messages.error(request, 'Attendance already submitted for today!')
            return redirect('/home')
        else:
            if action == 'present':
                attendance_record = attendance(username=username, status='Present', date=datetime.now().date(), time_in=datetime.now().time())
                attendance_record.save()
                return redirect('/home')
            elif action == 'absent':
                reason = request.POST.get('reason')
                attendance_record = attendance(username=username, status='Absent', date=datetime.now().date(), time_in=datetime.now().time(), reason=reason)
                attendance_record.save()
                return redirect('/home')
    return render(request, 'home.html')
    
# update_attendance
@login_required(login_url='log_in')
def update_attendance(request, id, action):
    update_att = attendance.objects.get(id=id)
    if action == 'approved':
        update_att.is_approved = True
        update_att.is_respond = True
        update_att.approved_date = datetime.now().date()
        update_att.save()
        return redirect('/attrequest')
    elif action == 'reject':
        update_att.is_approved = False
        update_att.is_respond = True
        update_att.approved_date = datetime.now().date()
        update_att.save()
        return redirect('/attrequest')
    return render(request, 'attrequest.html')

@login_required(login_url='log_in')
def edit_attendance(request, id, action):
    update_att = attendance.objects.get(id=id)
    if action == 'Present':
        update_att.archive_status = update_att.status
        update_att.status = 'Present'
        update_att.updated_at= datetime.now().date()
        update_att.save()
        return redirect('/dashboard')
    elif action == 'Absent':
        update_att.archive_status = update_att.status
        update_att.status = 'Absent'
        update_att.updated_at = datetime.now().date()
        update_att.save()
        return redirect('/dashboard')
    return render(request, 'attrequest.html')
    


# Subordinate's view
@login_required(login_url='log_in')
def subordinate_home(request):
    current_date = datetime.now().date()
    logged_in_user = request.user
    username = CustomUser.objects.get(username=logged_in_user.username)
    total_days = (current_date - username.joining_date).days
    holidays = holiday_list.objects.filter(date__range=[username.joining_date, current_date])
    holidays_count = holidays.count()
    total_working_days = total_days - holidays_count
    total_present = attendance.objects.filter(username=username, status='Present').count()
    present_percentage = (total_present / total_working_days) * 100
    user=username
    attendance_record = attendance.objects.filter(username=user, date=datetime.now().date())
    attendance_exist = attendance_record.exists()

    accounts_count=CustomUser.objects.filter(boss_name=logged_in_user.username,is_response=False,is_staff=False)

    logged_in_user = request.user
    accounts_count=CustomUser.objects.filter(boss_name=logged_in_user.username)
    user_email=accounts_count.values_list('email')
    attendance_request_count = attendance.objects.filter(username__email__in=user_email, is_respond=False)

    return render(request, 'subordinate/subordinate_home.html',{'logged_in_user':logged_in_user, 'attendance_record':attendance_record, 'attendance_exist':attendance_exist,'present_percentage':present_percentage,'total_present':total_present})

def subordinate_profile(request):
    return render(request, 'subordinate/subordinate_profile.html')

@login_required(login_url='log_in')
def subordinate_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        user.designation = request.POST.get('designation')
        user.department = request.POST.get('department')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.gender = request.POST.get('gender')
        user.office = request.POST.get('office')
        user.joining_date = request.POST.get('joining_date')
        user.address = request.POST.get('address')
        user.phone = request.POST.get('phone')
        user.email = request.POST.get('email')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('subordinate_profile')

    return render(request, 'subordinate/subordinate_profile_edit.html', {'user': user})

@login_required(login_url='log_in')
def subordinate_dashboard(request):
    logged_in_user = request.user
    accounts = CustomUser.objects.filter(username=logged_in_user.username)
    user_email = accounts.values_list('email')
    
    # Determine filter type (default to 'today' if not specified)
    filter_type = request.GET.get('filter', 'today')

    # Define date ranges based on filter type
    if filter_type == 'today':
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
    elif filter_type == '7d':
        start_date = datetime.now().date() - timedelta(days=7)
        end_date = datetime.now().date() + timedelta(days=1)
    elif filter_type == '30d':
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date() + timedelta(days=1)
    elif filter_type == '6m':
        start_date = datetime.now().date() - timedelta(days=30 * 6)
        end_date = datetime.now().date() + timedelta(days=1)
    elif filter_type == '1y':
        start_date = datetime.now().date() - timedelta(days=365)
        end_date = datetime.now().date() + timedelta(days=1)
    else:
        # Default to 'today' filter if invalid filter type
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)

    # Filter attendance records based on date range
    attendance_record = attendance.objects.filter(
        username__email__in=user_email,
        date__range=[start_date, end_date]
    )

    return render(request, 'subordinate/subordinate_dashboard.html', {
        'attendance_record': attendance_record,
        'accounts': accounts,
        'logged_in_user': logged_in_user,
        'user_email': user_email,
        'filter_type': filter_type
    })

@login_required(login_url='log_in')
def subordinate_attendance_submit(request, username, action):
    user= CustomUser.objects.get(username=username)
    user=user
    attendance_record = attendance.objects.filter(username=user, date=datetime.now().date())
    username = CustomUser.objects.get(username=username)
    if attendance_record.count() > 0:
        messages.error(request, 'Attendance already submitted for today!')
        return redirect('/subordinate_home')
    else:
        if action == 'present':
            attendance_record = attendance(username=username, status='Present', date=datetime.now().date(), time_in=datetime.now().time())
            attendance_record.save()
            return redirect('/subordinate_home')
        elif action == 'absent':
            reason = request.POST.get('reason')
            attendance_record = attendance(username=username, status='Absent', date=datetime.now().date(), time_in=datetime.now().time(), reason=reason)
            attendance_record.save()
            return redirect('/subordinate_home')
    return render(request, 'subordinate/subordinate_home.html')

@login_required(login_url='log_in')
def subordinate_attendance_submit(request, username, action):
    user= CustomUser.objects.get(username=username)
    user=user
    attendance_record = attendance.objects.filter(username=user, date=datetime.now().date())
    username = CustomUser.objects.get(username=username)
    if attendance_record.count() > 0:
        messages.error(request, 'Attendance already submitted for today!')
        return redirect('/subordinate_home')
    else:
        if action == 'present':
            attendance_record = attendance(username=username, status='Present', date=datetime.now().date(), time_in=datetime.now().time())
            attendance_record.save()
            return redirect('/subordinate_home')
        elif action == 'absent':
            reason = request.POST.get('reason')
            attendance_record = attendance(username=username, status='Absent', date=datetime.now().date(), time_in=datetime.now().time(), reason=reason)
            attendance_record.save()
            return redirect('/subordinate_home')
    return render(request, 'subordinate/subordinate_home.html')
def add_holiday(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        occasion = request.POST.get('occassion')
        holiday= holiday_list(date=date, occasion=occasion)
        holiday.save()
        messages.success(request, 'Holiday added successfully!')
        return redirect('/dashboard')
    return render(request, 'dashboard.html')

# # Edit Employee
# @login_required(login_url='log_in')
# def boss_edit(request,id):
#     boss_edit = CustomUser.objects.get(id=id)
#     if request.method == 'POST':
#         boss_edit.designation = request.POST.get('designation')
#         boss_edit.department = request.POST.get('department')
#         boss_edit.office = request.POST.get('office')
#         boss_edit.joining_date = request.POST.get('joining_date')
#         boss_edit.is_boss = request.POST.get('is_boss')

#         # boss_edit=CustomUser(designation=designation,department=department,office=office,joining_date=joining_date,is_boss=is_boss)

#         boss_edit.save()
#         messages.success(request, 'Employee details updated successfully!')
#         return redirect('view_details', id)

#     return render(request, 'boss_edit_page.html',{'boss_edit': boss_edit})

# def boss_edit_page(request, id):
#     user_em=CustomUser.objects.get(id=id)
#     return render(request, 'boss_edit_page.html',{'boss_edit':user_em})


# Edit Employee
@login_required(login_url='log_in')
def boss_edit(request, id):
    boss_edit = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        boss_edit.designation = request.POST.get('designation')
        boss_edit.department = request.POST.get('department')
        boss_edit.office = request.POST.get('office')
        boss_edit.joining_date = request.POST.get('joining_date')
        boss_edit.is_boss = request.POST.get('is_boss')

        boss_edit.save()
        return redirect('view_details', id=id)

    return render(request, 'boss_edit_page.html', {'boss_edit': boss_edit})

@login_required(login_url='log_in')
def boss_edit_page(request, id):
    boss_edit = CustomUser.objects.get(id=id)
    return render(request, 'boss_edit_page.html', {'boss_edit': boss_edit})


# @login_required(login_url='log_in')
# def export_attendance_to_excel(request):
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="attendance.xlsx"'

#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Attendance"

#     # Define the headings
#     columns = ['Employee Name', 'Username', 'Office', 'Designation', 'Date', 'Time In', 'Status', 'Remarks']
#     ws.append(columns)

#     # Retrieve the data
#     rows = attendance.objects.all().values_list(
#         'username__firstname', 'username__username', 'username__office',
#         'username__designation', 'date', 'time_in', 'status', 'archive_status'
#     )
#     for row in rows:
#         ws.append(row)

#     wb.save(response)
#     return response
