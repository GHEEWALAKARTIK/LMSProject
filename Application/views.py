from django.shortcuts import render, redirect
from Application.models import User, Leave
from django.contrib import messages
from datetime import datetime, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def Registration(request):
    if request.method == 'GET':
        return render(request, 'LR_Site/registration.html')
    else:
        error = False
        if len(request.POST['Name']) < 2:
            messages.error(request, "Surname must be 2 or more characters !")
            error = True

        elif (User.objects.filter(Name=request.POST['Name']).exists()):
            messages.error(request, "User-Name is already exist !")
            error = True

        elif (len(request.POST['Password']) < 5):
            messages.error(request, "Password must be 6 or more characters !")
            error = True

        elif (request.POST['Password'] != request.POST['ConfirmPassword']):
            messages.error(request, "Password or Confirm-Password must be same !")
            error = True

        if (error):
            return redirect('/Registration')

        else:
            Role = request.POST['Role']
            if(Role == 'EMPLOYEE'):
                Qry_User = User(Name=request.POST['Name'],
                                Role=request.POST['Role'],
                                Total_Leave=30,
                                Password=request.POST['Password'])
                Qry_User.save()
            else:
                Qry_User = User(Name=request.POST['Name'],
                                Role=request.POST['Role'],
                                Password=request.POST['Password'])
                Qry_User.save()
            return redirect('/')

def Login(request):
    if request.method == 'GET':
        return render(request, 'LR_Site/login.html')
    else:
        Qry_User_Login = ''
        Role = ''
        if(len(request.POST['Name']) < 2):
            messages.error(request, "Name must be 2 or more !")
            error = True
        else:
            try:
                error = False
                Qry_User_Login = User.objects.get(Name=request.POST['Name'])
                Role = Qry_User_Login.Role

                if Qry_User_Login.Password != request.POST['Password']:
                    messages.error(request, "Password is Incorrect !")
                    error = True

            except (User.DoesNotExist):
                messages.error(request, "Name is Incorrect !")
                error = True

        if error:
            return redirect('/')
        else:
            request.session['id'] = Qry_User_Login.UID
            request.session['name'] = Qry_User_Login.Name
            if(Role == 'ADMIN'):
                return redirect('/AdminHome')
            elif(Role == 'MANAGER'):
                return redirect('/ManagerHome')
            elif(Role == 'EMPLOYEE'):
                return redirect('/UserHome')

def Logout(request):
    request.session.flush()
    return redirect('/')

def UserHome(request):
    if request.method == 'GET':
        paginator = Leave.objects.all().order_by('-LID')
        page = request.GET.get('page', 1)
        Qry_Display_Leave = Paginator(paginator, 10)
        try:
            users = Qry_Display_Leave.page(page)
        except PageNotAnInteger:
            users = Qry_Display_Leave.page(1)
        except EmptyPage:
            users = Qry_Display_Leave.page(Qry_Display_Leave.num_pages)

        Qry_Display_User_Leave = User.objects.all()
        context = {
            'ID': request.session['id'],
            'Name': request.session['name'],
            'All_Leave': users,
            'All_User_Leave': Qry_Display_User_Leave,
        }
        return render(request, 'User_Site/userhome.html', context)
    else:
        SD = request.POST['FromDate']
        ED = request.POST['ToDate']
        FromDate = datetime.strptime(SD, '%Y-%m-%d')
        ToDate = datetime.strptime(ED, '%Y-%m-%d')

        SDate = FromDate.strftime("%d")
        EDate = ToDate.strftime("%d")

        Differance = int(EDate) - int(SDate) + 1

        i = 1
        while i <= Differance:
            Qry_Update_User_Total_Leave = User.objects.get(UID=request.POST['UID'])
            Total_Leave = Qry_Update_User_Total_Leave.Total_Leave
            Total_Remaining_Leave = Total_Leave - 1
            Qry_Update_User_Total_Leave.Total_Leave = Total_Remaining_Leave
            Qry_Update_User_Total_Leave.save()
            i += 1


        Qry_Insert_Leave = Leave(UID_id=request.POST['UID'],
                                 Start_Date=FromDate,
                                 End_Date=ToDate,
                                 Description=request.POST['Description'])
        Qry_Insert_Leave.save()
        return redirect('/UserHome')

def ManagerHome(request):
    if request.method == 'GET':
        paginator = Leave.objects.filter(Seen_By_Manager=False).order_by('-LID')
        page = request.GET.get('page', 1)
        Qry_Display_Leave = Paginator(paginator, 15)
        try:
            users = Qry_Display_Leave.page(page)
        except PageNotAnInteger:
            users = Qry_Display_Leave.page(1)
        except EmptyPage:
            users = Qry_Display_Leave.page(Qry_Display_Leave.num_pages)

        context = {
            'Name': request.session['name'],
            'All_Leave': users,
        }
        return render(request, 'Manager_Site/managerhome.html', context)

def Approve_User_Leave(request, id):
    Qry_Approve_User_Leave = Leave.objects.get(LID=id)
    Qry_Approve_User_Leave.Leave_Status = True
    Qry_Approve_User_Leave.Seen_By_Manager = True
    Qry_Approve_User_Leave.save()
    return redirect('/ManagerHome')

def Disapprove_User_Leave(request, id):
    Qry_Approve_User_Leave = Leave.objects.get(LID=id)
    Qry_Approve_User_Leave.Leave_Status = False
    Qry_Approve_User_Leave.Seen_By_Manager = True
    Qry_Approve_User_Leave.save()
    return redirect('/ManagerHome')

def AdminHome(request):
    paginator = Leave.objects.all().order_by('-UID')
    page = request.GET.get('page', 1)
    Qry_Display_Leave = Paginator(paginator, 10)
    try:
        users1 = Qry_Display_Leave.page(page)
    except PageNotAnInteger:
        users1 = Qry_Display_Leave.page(1)
    except EmptyPage:
        users1 = Qry_Display_Leave.page(Qry_Display_Leave.num_pages)

    paginator2 = User.objects.exclude(Role='ADMIN').all().order_by('-UID')
    page = request.GET.get('page', 1)
    Qry_Display_Leave = Paginator(paginator2, 10)
    try:
        users2 = Qry_Display_Leave.page(page)
    except PageNotAnInteger:
        users2 = Qry_Display_Leave.page(1)
    except EmptyPage:
        users2 = Qry_Display_Leave.page(Qry_Display_Leave.num_pages)

    context = {
        'Name': request.session['name'],
        'All_Leave': users1,
        'All_User': users2,
    }
    return render(request, 'Admin_Site/adminhome.html', context)