from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, reverse
from .models import users_all, faculty_all, title_all, users_history
from .forms import userAllForm, change_passForm
# Create your views here.
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
import random
import requests
from email_validate import validate


def generatePass():
    passwd = ''
    for x in range(16):
        passwd = passwd + random.choice(list(
            'abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ1234567890'))
    return passwd


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '3':
        return render(request, 'main/index.html')
    else:
        return redirect('login')


def register(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '3':
        error = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["exp_date"] == ""):
                _mutable = form.data._mutable
                form.data._mutable = True
                form.data["exp_date"] = datetime.now() + timedelta(weeks=288)
                form.data._mutable = _mutable
            _mutable = form.data._mutable
            form.data._mutable = True
            form.data["creator"] = request.COOKIES.get('username')
            generated_pass = generatePass()
            password = generated_pass
            password = make_password(password)
            r = requests.get(
                f"https://api.unisender.com/ru/api/sendEmail?format=json&api_key=6q6o8ud7w8sxs67oga6wedpichx4xogxr8x18uqe&email={form.data['email']}&sender_name=Support&sender_email=botcreationlab@gmail.com&subject=Your new password.&body=Your new password: {generated_pass}&list_id=1")
            form.data["passwd"] = password
            value = request.POST.getlist('title_id')
            lvladmin = users_all.adminRole(value[0])
            form.data["admin_level"] = lvladmin
            if (form.data["admin_level"] >= 3):
                form.data["admin"] = "y"
            form.data["title_id"] = value[0]
            form.data["passwd"] = password
            form.data._mutable = _mutable
            if (form.data["login"] != ""):
                if (form.data["document_id"] != ""):
                    if (form.data["lname"] != ""):
                        if (form.data["fname"] != ""):
                            if (form.data["mname"] != ""):
                                if (form.data["email"] != ""):
                                    if (validate(email_address=form.data["email"]) == True):
                                        if form.is_valid():
                                            users = users_all.objects.filter(login=form.data["login"])
                                            form.data._mutable = _mutable
                                            if (len(users) == 0):
                                                lol = form.save()
                                                history = users_history()
                                                history.user_id = lol.id
                                                history.date = datetime.now()
                                                history.action = "CREATION"
                                                history.creator = request.COOKIES.get('username')
                                                history.ip = get_client_ip(request)
                                                history.save()
                                                return redirect('home')
                                            else:
                                                error = "Заповніть ще раз. Такой логін вже існує."
                                        else:
                                            error = "Перевірте коректність заповлення форми."
                                    else:
                                        error = "Введіть коректний імейл"
                                else:
                                    error = "Заповніть імейл"
                            else:
                                error = "Заповніть по батькові."
                        else:
                            error = "Заповніть ім'я."
                    else:
                        error = "Заповніть прізвище."
                else:
                    error = "Заповніть номер посвідчення."
            else:
                error = "Заповніть ще раз. Ви не ввели логін."
            _mutable = form.data._mutable
            form.data._mutable = True
            form.data["exp_date"] = ""
            form.data._mutable = _mutable
            data = {
                'form': form,
                'error': error
            }
            return render(request, 'main/registration.html', data)

        form = userAllForm()
        data = {
            'form': form,
            'error': error
        }
        return render(request, 'main/registration.html', data)

    else:
        return redirect('login')


def find(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '3':
        users = ""
        error = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["fname"] != "" or form.data["login"] != "" or form.data["document_id"] != ""
                    or form.data["lname"] != "" or form.data["mname"] != "" or form.data["email"] != ""):
                users = users_all.search_all(users_all.objects.filter(fname__icontains=form.data["fname"])
                                             .filter(login__icontains=form.data["login"])
                                             .filter(document_id__icontains=form.data["document_id"])
                                             .filter(lname__icontains=form.data["lname"])
                                             .filter(mname__icontains=form.data["mname"])
                                             .filter(email__icontains=form.data["email"]))
                if (len(users) > 5):
                    users = []
                    error = "Уточніть запит"
                data = {
                    'form': form,
                    'info': users,
                    'error': error
                }
                return render(request, 'main/userfind.html', data)
            else:
                error = "Уведіть хоча б один із пунктів для пошуку"

        form = userAllForm()
        data = {
            'form': form,
            'info': users,
            'error': error
        }
        return render(request, 'main/userfind.html', data)
    else:
        return redirect('login')


def termlonger(request):
    error = ""
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '3':
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = users_all.search_all(users_all.objects.filter(login=form.data["login"]))
            if users != []:
                if form.data["exp_date"] != "":
                    exp_date_raw = form.data["exp_date"].split('/')
                    exp_date = datetime(int(exp_date_raw[2]), int(exp_date_raw[0]), int(exp_date_raw[1]))
                    if exp_date.timestamp() > datetime.now().timestamp():
                        user = users_all(id=users[0]["id"])
                        user.exp_date = exp_date
                        history = users_history()
                        history.user_id = users[0]["id"]
                        history.date = datetime.now()
                        history.action = "EXT_EXPIRE"
                        history.creator = request.COOKIES.get('username')
                        history.ip = get_client_ip(request)
                        history.save()
                        user.save(update_fields=['exp_date'])
                        error = "Успішно встановлено"
                    else:
                        error = "Дата не може бути за минулий період"
                else:
                    error = "Уведіть правильну дату"
            else:
                error = "Уведіть правильний логін"

        form = userAllForm()
        data = {
            'form': form,
            'error': error
        }
        return render(request, 'main/termlonger.html', data)
    else:
        return redirect('login')


def changepass(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '3':
        success = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = users_all.search_all(users_all.objects.filter(login=form.data["login"]))
            if (users != []):
                generated_pass = generatePass()
                password = generated_pass
                password = make_password(password)
                r = requests.get(
                    f"https://api.unisender.com/ru/api/sendEmail?format=json&api_key=6q6o8ud7w8sxs67oga6wedpichx4xogxr8x18uqe&email={users[0]['email']}&sender_name=Support&sender_email=botcreationlab@gmail.com&subject=Your new password.&body=Your new password: {generated_pass}&list_id=1")
                user = users_all(id=users[0]["id"])
                user.passwd = password
                success = "Успішно змінено"
                history = users_history()
                history.user_id = users[0]["id"]
                history.date = datetime.now()
                history.action = "CHPASS"
                history.creator = request.COOKIES.get('username')
                history.ip = get_client_ip(request)
                history.save()
                user.save(update_fields=['passwd'])
            else:
                success = "Юзера не існує"
        form = change_passForm()
        data = {
            'form': form,
            'success': success
        }
        return render(request, 'main/changepass.html', data)

    else:
        return redirect('login')


def change_own_pass(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and (request.COOKIES.get('iqlvl') == '2' or
            request.COOKIES.get('iqlvl') == '3'):
        success = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = users_all.search_all(users_all.objects.filter(login=request.COOKIES.get('username')))
            if (form.data["password"] == form.data["repassword"]):
                password = form.data["password"]
                password = make_password(password)
                user = users_all(id=users[0]["id"])
                user.passwd = password
                success = "Пароль успішно змінено"
                history = users_history()
                history.user_id = users[0]["id"]
                history.date = datetime.now()
                history.action = "CHPASS"
                history.creator = request.COOKIES.get('username')
                history.ip = get_client_ip(request)
                history.save()
                user.save(update_fields=['passwd'])
            else:
                success = "Паролі не співпадають"
        form = change_passForm()
        data = {
            'form': form,
            'success': success,
            'iqlvl': request.COOKIES.get('iqlvl')
        }
        return render(request, 'main/ownchangepass.html', data)

    else:
        return redirect('login')


def changeownpassuser(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '2':
        success = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = users_all.search_all(users_all.objects.filter(login=request.COOKIES.get('username')))
            if (form.data["password"] == form.data["repassword"]):
                password = form.data["password"]
                password = make_password(password)
                user = users_all(id=users[0]["id"])
                user.passwd = password
                success = "Пароль успішно змінено"
                history = users_history()
                history.user_id = users[0]["id"]
                history.date = datetime.now()
                history.action = "CHPASS"
                history.creator = request.COOKIES.get('username')
                history.ip = get_client_ip(request)
                history.save()
                user.save(update_fields=['passwd'])
            else:
                success = "Паролі не співпадають"
        form = change_passForm()
        data = {
            'form': form,
            'success': success
        }
        return render(request, 'main/ownchangepassuser.html', data)

    else:
        return redirect('login')


def history(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '3':
        info = []
        error = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            login = form.data["login"]
            if (login != ""):
                logD = users_all.objects.all()
                idOfuser = -1
                for el in logD:
                    if (login == el.login):
                        idOfuser = el.id
                        break
                if (idOfuser != -1):
                    history = users_history.objects.all()
                    for el in history:
                        if (idOfuser == el.user_id):
                            info.append({
                                "date": el.date,
                                "action": el.action,
                                "creator": el.creator,
                                "reason": el.reason,
                                "ip": el.ip
                            })
                else:
                    error = "За таким логіном користувача не знайдено"
            else:
                error = "Ви не ввели логін"

        form = userAllForm()
        data = {
            'form': form,
            'info': info,
            'error': error
        }
        return render(request, 'main/history.html', data)
    else:
        return redirect('login')


def login(request):
    if not 'login_status' in request.COOKIES and not 'username' in request.COOKIES:
        info = ""
        if request.method == "GET":
            form = userAllForm()
            data = {
                'form': form,
                'info': info
            }
            response = render(request, 'main/login.html', data)
            return response

        if request.method == "POST":
            form = userAllForm(request.POST)
            login = form.data["login"]
            password = form.data["passwd"]
            users = users_all.search_all(users_all.objects.filter(login=form.data["login"]))
            logD = users_all.objects.all()
            for el in logD:
                if login == el.login:
                    if check_password(password, el.passwd):
                        if el.exp_date.timestamp() > datetime.now().timestamp():
                            if el.admin_level >= 3:
                                response = render(request, 'main/index.html')
                                response.set_cookie('username', login)
                                response.set_cookie('login_status', True)
                                response.set_cookie('iqlvl', el.admin_level)
                                return response
                            elif el.admin_level == 2:
                                response = render(request, 'main/user_home.html')
                                response.set_cookie('username', login)
                                response.set_cookie('login_status', True)
                                response.set_cookie('iqlvl', el.admin_level)
                                return response
                            else:
                                info = "У вас недостатньо прав на вхід."
                                break
                        else:
                            info = "Термін дії аккаунту сплив. Зверніться до адміністратора."
                            break
                    else:
                        info = "Неправильний пароль."
                        break
                else:
                    info = "Такого логіну не існує"
        form = userAllForm()
        data = {
            'form': form,
            'info': info
        }
        response = render(request, 'main/login.html', data)
        return response
    else:
        if request.COOKIES.get('iqlvl') == '3':
            response = redirect('home')
            return response
        elif request.COOKIES.get('iqlvl') == '2':
            response = redirect('uhome')
            return response

"""def remind_password(request):
    if not 'login_status' in request.COOKIES and not 'username' in request.COOKIES:
        info = ""
        if request.method == "GET":
            form = userAllForm()
            data = {
                'form': form,
                'info': info
            }
            response = render(request, 'main/login.html', data)
            return response

        if request.method == "POST":
            form = userAllForm(request.POST)
            login = form.data["login"]
            logD = users_all.objects.all()
            for el in logD:
                if login == el.login:

                else:
                    info = "Такого логіну не існує"
        form = userAllForm()
        data = {
            'form': form,
            'info': info
        }
        response = render(request, 'main/login.html', data)
        return response
    else:
        response = render(request, 'main/index.html')
        return response
"""


def userhome(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '2':
        return render(request, 'main/user_home.html')
    else:
        return redirect('login')



def findstuff(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES and request.COOKIES.get('iqlvl') == '2':
        users = ""
        error = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["fname"] != "" or form.data["lname"] != "" or form.data["mname"] != ""
                    or form.data["email"] != ""):
                users = users_all.search_all(users_all.objects.filter(admin_level=3)
                                             .filter(fname__icontains=form.data["fname"])
                                             .filter(lname__icontains=form.data["lname"])
                                             .filter(mname__icontains=form.data["mname"])
                                             .filter(email__icontains=form.data["email"]))
                if (len(users) > 5):
                    users = []
                    error = "Уточніть запит"
                data = {
                    'form': form,
                    'info': users,
                    'error': error
                }
                return render(request, 'main/userfind_user.html', data)
            else:
                error = "Уведіть хоча б один із пунктів для пошуку"

        form = userAllForm()
        data = {
            'form': form,
            'info': users,
            'error': error
        }
        return render(request, 'main/userfind_user.html', data)
    else:
        return redirect('login')


def logout(request):
    responce = HttpResponseRedirect(reverse('login'))
    responce.delete_cookie('username')
    responce.delete_cookie('login_status')
    responce.delete_cookie('iqlvl')
    return responce
