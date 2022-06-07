from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, reverse
from .models import UsersAll, UsersHistory, DeptAll, TitleAll, UsersAccessGroup, RestorePassword
from .forms import userAllForm, change_passForm, remindpass, usersupdateform, Users_access_group_form
# Create your views here.
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
import random
import requests
import hashlib
from email_validate import validate
from django.views.generic import UpdateView
import uuid


def generatePass():
    passwd = ''
    for x in range(16):
        passwd = passwd + random.choice(list(
            'abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ1234567890'))
    return passwd


def generateTestCode():
    passwd = ''
    for x in range(5):
        passwd = passwd + random.choice(list(
            '1234567890/'))
    return passwd


def hashMDPass(password):
    hash_object = hashlib.md5(password.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


def delete_cookies():
    responce = HttpResponseRedirect(reverse('login'))
    responce.delete_cookie('username')
    responce.delete_cookie('login_status')
    responce.delete_cookie('iqlvl')
    return responce


def create_cookies(request, n, login, path, data):
    response = render(request, path, data)
    response.set_cookie('username', login, expires=datetime.utcnow() + timedelta(hours=1))
    response.set_cookie('login_status', True, expires=datetime.utcnow() + timedelta(hours=1))
    response.set_cookie('iqlvl', n, expires=datetime.utcnow() + timedelta(hours=1))
    return response


def check_cookies(login, status):
    logD = UsersAll.objects.all()
    checklogin = False
    checkSession = False
    for el in logD:
        if el.login == login:
            checklogin = True
            break
    if status:
        checkSession = True
    if checklogin and checkSession:
        return True
    else:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        data = {
            'lvl': int(request.COOKIES.get('iqlvl'))
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'), 'main/index.html',
                              data)
    else:
        return delete_cookies()


def register(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        error = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["exp_date"] == ""):
                _mutable = form.data._mutable
                form.data._mutable = True
                form.data["exp_date"] = datetime.now().date() + timedelta(weeks=288)
                form.data._mutable = _mutable
            _mutable = form.data._mutable
            form.data._mutable = True
            form.data["creator"] = request.COOKIES.get('username')
            value = request.POST.getlist('title_id')
            lvladmin = UsersAll.adminRole(value[0])
            form.data["admin_level"] = lvladmin
            if (form.data["admin_level"] == 4):
                form.data["admin"] = "y"
                form.data["operator"] = "y"
                form.data["mgroup_id"] = 2
            else:
                form.data["admin"] = "n"
                form.data["operator"] = "n"
                form.data["mgroup_id"] = 1

            form.data["title_id"] = value[0]
            if form.data["title_id"] == "":
                form.data["title_id"] = 1
            else:
                form.data["title_id"] = value[0]
            if form.data["dept_id"] == "":
                form.data["dept_id"] = 1
            form.data["state"] = 'OPEN'
            generated_pass = generatePass()
            password = generated_pass
            password = hashMDPass(password)
            form.data["passwd"] = password
            form.data._mutable = _mutable
            if (form.data["login"] != "" and form.data["login"] != "-"):
                if (form.data["document_id"] != "" and form.data["login"] != "-"):
                    if (form.data["lname"] != "" and form.data["login"] != "-"):
                        if (form.data["fname"] != "" and form.data["login"] != "-"):
                            if (form.data["mname"] != "" and form.data["login"] != "-"):
                                if (form.data["email"] != "" and form.data["login"] != "-"):
                                    if (validate(email_address=form.data["email"]) == True):
                                        _mutable = form.data._mutable
                                        form.data._mutable = True
                                        for el in form.data.keys():
                                            if form.data[el] == "":
                                                form.data[el] = "-"
                                        form.data._mutable = _mutable
                                        if form.is_valid():
                                            users = UsersAll.objects.filter(login=form.data["login"])
                                            id_dept = DeptAll.objects.all()
                                            id_title = TitleAll.objects.all()
                                            dept_number = 1
                                            for el in id_dept:
                                                if el == form.cleaned_data["dept_id"]:
                                                    break
                                                dept_number += 1
                                            title_number = 1
                                            for el in id_title:
                                                if el == form.cleaned_data["title_id"]:
                                                    break
                                                title_number += 1

                                            form.data._mutable = _mutable

                                            if (len(users) == 0):
                                                formForSave = UsersAll(login=form.cleaned_data["login"],
                                                                       document_id=form.cleaned_data["document_id"],
                                                                       contr_quest=form.cleaned_data["contr_quest"],
                                                                       contr_answ=form.cleaned_data["contr_answ"],
                                                                       lname=form.cleaned_data["lname"].encode(
                                                                           'cp1251').decode('latin-1'),
                                                                       fname=form.cleaned_data["fname"].encode(
                                                                           'cp1251').decode('latin-1'),
                                                                       mname=form.cleaned_data["mname"].encode(
                                                                           'cp1251').decode('latin-1'),
                                                                       dept_id=dept_number,
                                                                       title_id=title_number,
                                                                       title=form.cleaned_data["title"].encode(
                                                                           'cp1251').decode('latin-1'),
                                                                       email=form.cleaned_data["email"],
                                                                       phone=form.cleaned_data["phone"],
                                                                       welcome_msg=form.cleaned_data["welcome_msg"],
                                                                       exp_date=form.cleaned_data["exp_date"],
                                                                       admin_level=form.cleaned_data["admin_level"],
                                                                       admin=form.cleaned_data["admin"],
                                                                       mgroup_id=form.cleaned_data["mgroup_id"],
                                                                       operator=form.cleaned_data["operator"],
                                                                       state=form.cleaned_data["state"],
                                                                       creator=form.cleaned_data["creator"],
                                                                       passwd=form.cleaned_data["passwd"],
                                                                       )
                                                formForSave.save()
                                                r = requests.get(
                                                    f"https://api.unisender.com/ru/api/sendEmail?format=json&api_key=6q6o8ud7w8sxs67oga6wedpichx4xogxr8x18uqe&email={form.data['email']}&sender_name=Support&sender_email=botcreationlab@gmail.com&subject=Your new password.&body=Your new password: {generated_pass}&list_id=1")

                                                user = UsersAll.search_all(
                                                    UsersAll.objects.filter(login=form.data["login"]))
                                                history = UsersHistory()
                                                history.user_id = user[0]['id']
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

            req_params = {
                'login': 'Логін',
                'document_id': 'Номер документа',
                'lname': 'Прізвище',
                'fname': "Ім`я",
                'mname': "По батькові",
                'email': "Імейл"
            }
            tables = []
            for i in req_params.keys():
                if form.data[i] == '':
                    tables.append(req_params[i])

            if error == "":
                error = "Ви не заповнили " + ', '.join(tables)
            _mutable = form.data._mutable
            form.data._mutable = True
            form.data["exp_date"] = ""
            form.data._mutable = _mutable
            data = {
                'form': form,
                'lvl': int(request.COOKIES.get('iqlvl')),
                'error': error
            }
            return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                  'main/registration.html', data)

        form = userAllForm()
        data = {
            'form': form,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'error': error
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/registration.html', data)

    else:
        return delete_cookies()


def find(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        users = ""
        error = ""
        info_show = False
        searching_users = []
        if request.method == "POST":
            form = userAllForm(request.POST)
            try:
                if (form.data["fname"] != "" or form.data["login"] != "" or form.data["document_id"] != ""
                        or form.data["lname"] != "" or form.data["mname"] != "" or form.data["email"] != ""):
                    if int(request.COOKIES.get('iqlvl')) == 2:
                        users = UsersAll.search_all(
                            UsersAll.objects.filter(
                                fname__icontains=form.data["fname"].encode('cp1251').decode('latin-1'))
                                .filter(login__icontains=form.data["login"])
                                .filter(document_id__icontains=form.data["document_id"])
                                .filter(lname__icontains=form.data["lname"].encode('cp1251').decode('latin-1'))
                                .filter(mname__icontains=form.data["mname"].encode('cp1251').decode('latin-1'))
                                .filter(email__icontains=form.data["email"])
                                .filter(dept_id=UsersAll.objects.get(login=request.COOKIES.get('username')).dept_id))
                    else:
                        users = UsersAll.search_all(
                            UsersAll.objects.filter(
                                fname__icontains=form.data["fname"].encode('cp1251').decode('latin-1'))
                                .filter(login__icontains=form.data["login"])
                                .filter(document_id__icontains=form.data["document_id"])
                                .filter(lname__icontains=form.data["lname"].encode('cp1251').decode('latin-1'))
                                .filter(mname__icontains=form.data["mname"].encode('cp1251').decode('latin-1'))
                                .filter(email__icontains=form.data["email"]))
                    if users != []:
                        if (len(users) > 5):
                            searching_users = []
                            error = "Уточніть запит"
                        else:
                            for i in range(0, len(users)):
                                for el in users[i].keys():
                                    if isinstance(users[i][el], str):
                                        users[i][el] = users[i][el].encode('latin-1').decode('cp1251')
                            info_show = True
                            for el in users:
                                el["dept_id"] = DeptAll.objects.get(dept_id=el["dept_id"])
                                searching_users.append(el)
                    else:
                        error = "За такими данними користувача не знайдено."
                    data = {
                        'form': form,
                        'info': searching_users,
                        'error': error,
                        'lvl': int(request.COOKIES.get('iqlvl')),
                        'show': info_show
                    }
                    return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                          'main/userfind.html', data)
                else:
                    error = "Уведіть хоча б один із пунктів для пошуку"
            except:
                error = "Ви ввели недопустимі символи"
        form = userAllForm()
        data = {
            'form': form,
            'info': users,
            'error': error,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'show': info_show
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/userfind.html', data)
    else:
        return delete_cookies()


def termlonger(request):
    error = ""
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = UsersAll.search_all(
                UsersAll.objects.filter(login=form.data["login"].encode('cp1251').decode('latin-1')))
            if users != []:
                if form.data["exp_date"] != "":
                    exp_date_raw = form.data["exp_date"].split('/')
                    exp_date = datetime(int(exp_date_raw[2]), int(exp_date_raw[0]), int(exp_date_raw[1]))
                    if exp_date.timestamp() > datetime.now().timestamp():
                        user = UsersAll(id=users[0]["id"])
                        user.exp_date = exp_date
                        history = UsersHistory()
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
            'lvl': int(request.COOKIES.get('iqlvl')),
            'error': error
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/termlonger.html', data)
    else:
        return delete_cookies()


def changepass(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        success = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = UsersAll.search_all(UsersAll.objects.filter(login=form.data["login"]))
            if users != []:
                generated_pass = generatePass()
                password = generated_pass
                password = hashMDPass(password)
                r = requests.get(
                    f"https://api.unisender.com/ru/api/sendEmail?format=json&api_key=6q6o8ud7w8sxs67oga6wedpichx4xogxr8x18uqe&email={users[0]['email']}&sender_name=Support&sender_email=botcreationlab@gmail.com&subject=Your new password.&body=Your new password: {generated_pass}&list_id=1")
                user = UsersAll(user_id=users[0]["id"])
                user.passwd = password
                success = "Успішно змінено"
                history = UsersHistory()
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
            'lvl': int(request.COOKIES.get('iqlvl')),
            'success': success
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/changepass.html', data)
    else:
        return delete_cookies()


def change_own_pass(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        success = ""
        history = UsersHistory.objects.all()
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = UsersAll.search_all(UsersAll.objects.filter(login=request.COOKIES.get('username')))
            if form.data["password"] == form.data["repassword"]:
                if (len(form.data["password"]) >= 8):
                    password = form.data["password"]
                    password = hashMDPass(password)
                    user = UsersAll(user_id=users[0]["id"])
                    user.passwd = password
                    success = "Пароль успішно змінено."
                    history = UsersHistory()
                    history.user_id = users[0]["id"]
                    history.date = datetime.now()
                    history.action = "CHPASS"
                    history.creator = request.COOKIES.get('username')
                    history.ip = get_client_ip(request)
                    history.save()
                    user.save(update_fields=['passwd'])
                else:
                    success = "Мінімальна довжина паролю 8 символів."
            else:
                success = "Паролі не співпадають."
        form = change_passForm()
        data = {
            'form': form,
            'success': success,
            'lvl': int(request.COOKIES.get('iqlvl'))
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/ownchangepass.html', data)

    else:
        return delete_cookies()


def changeownpassuser(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) == 1:
        success = ""
        if request.method == "POST":
            form = userAllForm(request.POST)
            users = UsersAll.search_all(UsersAll.objects.filter(login=request.COOKIES.get('username')))
            if (form.data["password"] == form.data["repassword"]):
                if (len(form.data["password"]) >= 8):
                    password = form.data["password"]
                    password = hashMDPass(password)
                    user = UsersAll(user_id=users[0]["id"])
                    user.passwd = password
                    success = "Пароль успішно змінено."
                    history = UsersHistory()
                    history.user_id = users[0]["id"]
                    history.date = datetime.now()
                    history.action = "CHPASS"
                    history.creator = request.COOKIES.get('username')
                    history.ip = get_client_ip(request)
                    history.save()
                    user.save(update_fields=['passwd'])
                else:
                    success = "Мінімальна довжина паролю 8 символів."
            else:
                success = "Паролі не співпадають"
        form = change_passForm()
        data = {
            'form': form,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'success': success
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/ownchangepassuser.html', data)

    else:
        return delete_cookies()


def history(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        info = []
        error = ""
        info_show = False
        if request.method == "POST":
            form = userAllForm(request.POST)
            login = form.data["login"]
            if (login != ""):
                logD = UsersAll.objects.all()
                idOfuser = -1
                for el in logD:
                    if (login == el.login):
                        idOfuser = el.user_id
                        break
                if (idOfuser != -1):
                    history = UsersHistory.objects.all()
                    for el in history:
                        if (idOfuser == el.user_id):
                            if el.reason != None:
                                if len(el.reason) > 50:
                                    el.reason = "Дивись детальніше"
                            info.append({
                                "date": el.date.strftime("%H:%M %d-%m-%Y"),
                                "action": el.action,
                                "creator": el.creator,
                                "reason": el.reason,
                                "ip": el.ip,
                                'id': el.id
                            })
                    if info == []:
                        error = "Історії за цим користувачем не знайдено"
                    else:
                        info_show = True
                else:
                    error = "За таким логіном користувача не знайдено"
            else:
                error = "Ви не ввели логін"

        form = userAllForm()
        data = {
            'form': form,
            'info': info,
            'error': error,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'show': info_show
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/history.html', data)
    else:
        return delete_cookies()


def login(request):
    if not check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')):
        if 'timePass' in request.COOKIES:
            info = "Посилання на відновлення паролю, відправлено на пошту"
        else:
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
            users = UsersAll.search_all(UsersAll.objects.filter(login=form.data["login"]))
            logD = UsersAll.objects.all()
            for el in logD:
                if login == el.login:
                    if request.COOKIES.get('timePass') == None:
                        timepass = ""
                    else:
                        timepass = request.COOKIES.get('timePass')
                    if hashMDPass(password) == el.passwd:
                        if el.exp_date.timestamp() > datetime.now().timestamp():
                            data = {
                                'lvl': el.admin_level
                            }
                            if el.admin_level >= 2:
                                return create_cookies(request, el.admin_level, login, 'main/index.html', data)
                            elif el.admin_level == 1:
                                return create_cookies(request, el.admin_level, login, 'main/user_home.html', data)
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
        if int(request.COOKIES.get('iqlvl')) >= 2:
            response = redirect('home')
            return response
        elif int(request.COOKIES.get('iqlvl')) < 2:
            response = redirect('user_home')
            return response


def remind_password(request):
    if not check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')):
        info = ""
        test_code = generateTestCode()
        try:
            if request.method == "POST":
                form = remindpass(request.POST)
                users = UsersAll.search_all(UsersAll.objects.filter(login=form.data["login"]))
                login = form.data["login"]
                id_document = form.data["document_id"]
                logD = UsersAll.objects.all()
                if login != "":
                    for el in logD:
                        if login == el.login:
                            if check_password(id_document, request.COOKIES.get('testCode')):
                                form = userAllForm()
                                info = "Посилання на відновлення паролю, відправлено на пошту"
                                uuid_code = uuid.uuid4().hex
                                data = {
                                    'form': form,
                                    'info': info
                                }
                                generated_pass = f'http://diplom.botcreationlab.com/recovery/{uuid_code}'
                                response = redirect('login')
                                response.set_cookie('timePass', make_password(generated_pass),
                                                    expires=datetime.utcnow() + timedelta(minutes=1))
                                recovery_record = RestorePassword()
                                recovery_record.user = UsersAll.objects.get(login=users[0]['login']).user_id
                                recovery_record.exp_date = datetime.now() + timedelta(minutes=15)
                                recovery_record.created_date = datetime.now()
                                recovery_record.ip = get_client_ip(request)
                                recovery_record.temporary_pass = uuid_code
                                recovery_record.save()

                                r = requests.get(
                                    f"https://api.unisender.com/ru/api/sendEmail?format=json&api_key=6q6o8ud7w8sxs67oga6wedpichx4xogxr8x18uqe&email={users[0]['email']}&sender_name=Support&sender_email=botcreationlab@gmail.com&subject=New password .&body=Create new password by this url: {generated_pass}&list_id=1")

                                return response
                            else:
                                info = "Не правильно набраний код."
                                break
                        else:
                            info = "Такого логіну не існує."
                else:
                    info = "Ви не ввели логін."
                test_code = generateTestCode()
                _mutable = form.data._mutable
                form.data._mutable = True
                form.data["document_id"] = ""
                form.data._mutable = _mutable
                data = {
                    'form': form,
                    'info': info,
                    'test': test_code
                }
                response = render(request, 'main/remind_password.html', data)
                response.set_cookie('testCode', make_password(test_code), expires=datetime.utcnow() + timedelta(minutes=2))
                return response
        except:
            pass
        form = remindpass()
        data = {
            'form': form,
            'info': info,
            'test': test_code
        }
        response = render(request, 'main/remind_password.html', data)
        response.set_cookie('testCode', make_password(test_code), expires=datetime.utcnow() + timedelta(minutes=2))
        return response
    else:
        response = redirect('login')
        return response


def userhome(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) and request.COOKIES.get(
            'iqlvl') == '1':
        data = {}
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/user_home.html', data)
    else:
        return delete_cookies()


def findstuff(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) == 1:
        users = ""
        error = ""
        show = False
        searching_users = []
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["fname"] != "" or form.data["lname"] != "" or form.data["mname"] != ""
                    or form.data["email"] != ""):
                users = UsersAll.search_all(UsersAll.objects.exclude(admin_level=1)
                                            .exclude(admin_level=0)
                                            .filter(fname__icontains=form.data["fname"])
                                            .filter(lname__icontains=form.data["lname"])
                                            .filter(mname__icontains=form.data["mname"])
                                            .filter(email__icontains=form.data["email"]))
                if users != []:
                    if (len(users) > 5):
                        searching_users = []
                        error = "Уточніть запит"
                    else:
                        for i in range(0, len(users)):
                            for el in users[i].keys():
                                if isinstance(users[i][el], str):
                                    users[i][el] = users[i][el].encode('latin-1').decode('cp1251')
                        show = True
                        for el in users:
                            el["dept_id"] = DeptAll.objects.get(dept_id=el["dept_id"])
                            searching_users.append(el)
                else:
                    error = "За такими данними користувача не знайдено."
                data = {
                    'form': form,
                    'info': searching_users,
                    'lvl': int(request.COOKIES.get('iqlvl')),
                    'error': error,
                    'show': show
                }
                return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                      'main/userfind_user.html', data)
            else:
                error = "Уведіть хоча б один із пунктів для пошуку"

        form = userAllForm()
        data = {
            'form': form,
            'info': users,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'error': error,
            'show': show
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/userfind_user.html', data)
    else:
        return delete_cookies()


def logout(request):
    return delete_cookies()


def UserUpdateView(request, pk):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 1:
        error = ""
        base_template = ""
        if int(request.COOKIES.get('iqlvl')) >= 2:
            base_template = "main/layout.html"
        else:
            base_template = "main/userlayout.html"
        only_view = False
        template = 'main/user_update.html'
        get_user = UsersAll.objects.get(pk=pk)
        infoAboutUser = UsersAll.show_all(UsersAll.objects.filter(login=get_user.login))[0]
        infoAboutUser["dept_id"] = DeptAll.objects.get(pk=infoAboutUser["dept_id"])
        infoAboutUser["title_id"] = TitleAll.objects.get(pk=infoAboutUser["title_id"])
        infoAboutUser["exp_date"] = infoAboutUser["exp_date"].strftime("%d-%m-%Y")
        if request.method == "POST":
            changes = []
            form = userAllForm(request.POST)
            prevForm = UsersAll.show_all(UsersAll.objects.filter(login=get_user.login))[0]
            _mutable = form.data._mutable
            form.data._mutable = True
            check_email = True
            try:
                if form.data["dept_id"] != "":
                    if int(form.data["dept_id"]) != int(
                            DeptAll.objects.get(dept_ename=infoAboutUser["dept_id"]).dept_id):
                        changes.append(
                            f"Dept changed from {DeptAll.objects.get(pk=prevForm['dept_id'])} to {DeptAll.objects.get(pk=int(form.data['dept_id']))}")
                        prevForm['dept_id'] = form.data["dept_id"]
            except:
                pass
            try:
                if form.data["state"] != infoAboutUser["state"] \
                        and form.data["state"] != "":
                    changes.append(
                        f"State changed from {prevForm['state']} to {form.data['state']}")
                    prevForm['state'] = form.data["state"]
            except:
                pass
            try:
                if form.data["fname"] != infoAboutUser["fname"] and form.data["fname"] != "":
                    changes.append(
                        f"Name changed from {prevForm['fname']} to {form.data['fname']}")
                    prevForm['fname'] = form.data["fname"]
            except:
                pass
            try:
                if form.data["lname"] != infoAboutUser["lname"] and form.data["lname"] != "":
                    changes.append(
                        f"Surname changed from {prevForm['lname']} to {form.data['lname']}")
                    prevForm['lname'] = form.data["lname"]
            except:
                pass
            try:
                if form.data["mname"] != infoAboutUser["mname"] and form.data["mname"] != "":
                    changes.append(
                        f"Middle name changed from {prevForm['mname']} to {form.data['mname']}")
                    prevForm['mname'] = form.data["mname"]
            except:
                pass
            try:
                if form.data["contr_quest"] != infoAboutUser["contr_quest"] and form.data["contr_quest"] != "":
                    changes.append(
                        f"Control question changed from {prevForm['contr_quest']} to {form.data['contr_quest']}")
                    prevForm['contr_quest'] = form.data["contr_quest"]
            except:
                pass
            try:
                if form.data["contr_answ"] != infoAboutUser["contr_answ"] and form.data["contr_answ"] != "":
                    changes.append(
                        f"Control answer changed from {prevForm['contr_answ']} to {form.data['contr_answ']}")
                    prevForm['contr_answ'] = form.data["contr_answ"]
            except:
                pass
            try:
                if form.data["title"] != infoAboutUser["title"] and form.data["title"] != "":
                    changes.append(
                        f"Title changed from {prevForm['title']} to {form.data['title']}")
                    prevForm['title'] = form.data["title"]
            except:
                pass
            try:
                if form.data["email"] != infoAboutUser["email"] and form.data["email"] != "":
                    if not validate(form.data['email']):
                        check_email = False
                    else:
                        changes.append(
                            f"Email changed from {prevForm['email']} to {form.data['email']}")
                        prevForm['email'] = form.data["email"]
            except:
                pass
            try:
                if form.data["phone"] != infoAboutUser["phone"] and form.data["phone"] != "":
                    changes.append(
                        f"Phone changed from {prevForm['phone']} to {form.data['phone']}")
                    prevForm['phone'] = form.data["phone"]
            except:
                pass
            try:
                if form.data["exp_date"] != infoAboutUser["exp_date"] and form.data["exp_date"] != "":
                    changes.append(
                        f"Exp. date changed from {prevForm['exp_date']} to {form.data['exp_date']}")
                    exp_date_raw = form.data["exp_date"].split('/')
                    form.data["exp_date"] = datetime(int(exp_date_raw[2]), int(exp_date_raw[0]), int(exp_date_raw[1]))
                    prevForm['exp_date'] = form.data["exp_date"]
            except:
                pass
            try:
                if form.data["welcome_msg"] != infoAboutUser["welcome_msg"] and form.data["welcome_msg"] != "":
                    changes.append(
                        f"Welcome message changed from {prevForm['welcome_msg']} to {form.data['welcome_msg']}")
                    prevForm['welcome_msg'] = form.data["welcome_msg"]
            except:
                pass
            try:
                if form.data["admin"] != infoAboutUser["admin"] and form.data["admin"] != "":
                    changes.append(
                        f"Admin message changed from {prevForm['admin']} to {form.data['admin']}")
                    prevForm['admin'] = form.data["admin"]
            except:
                pass
            try:
                if form.data["document_id"] != infoAboutUser["document_id"] and form.data["document_id"] != "":
                    changes.append(
                        f"Document_id message changed from {prevForm['document_id']} to {form.data['document_id']}")
                    prevForm['document_id'] = form.data["document_id"]
            except:
                pass
            try:
                if form.data["operator"] != infoAboutUser["operator"] and form.data["operator"] != "":
                    changes.append(
                        f"Operator message changed from {prevForm['operator']} to {form.data['operator']}")
                    prevForm['operator'] = form.data["operator"]
            except:
                pass
            try:
                if form.data["mgroup_id"] != infoAboutUser["mgroup_id"] and form.data["mgroup_id"] != "":
                    changes.append(
                        f"Mgroup_id message changed from {prevForm['mgroup_id']} to {form.data['mgroup_id']}")
                    prevForm['mgroup_id'] = form.data["mgroup_id"]
            except:
                pass
            try:
                if form.data["title_id"] != "":
                    if int(form.data["title_id"]) != int(
                            TitleAll.objects.get(title_ename=infoAboutUser["title_id"]).title_id):
                        changes.append(
                            f"Job changed from {TitleAll.objects.get(pk=prevForm['title_id'])} to {TitleAll.objects.get(pk=int(form.data['title_id']))}")
                        prevForm['title_id'] = form.data["title_id"]
            except:
                pass
            try:
                if form.data["admin_level"] != infoAboutUser["admin_level"] and form.data["admin_level"] != "":
                    if int(form.data["admin_level"]) <= int(request.COOKIES.get('iqlvl')):
                        changes.append(
                            f"Admin_level message changed from {prevForm['admin_level']} to {form.data['admin_level']}")
                        prevForm['admin_level'] = form.data["admin_level"]
                    else:
                        error = "Ви не можете змінити рівень адміну на вищий за свій."
            except:
                pass
            if error == "":
                if check_email:
                    if changes != []:
                        updateUser = UsersAll(user_id=pk,
                                              login=prevForm['login'],
                                              document_id=prevForm['document_id'],
                                              contr_quest=prevForm['contr_quest'].encode('cp1251').decode('latin-1'),
                                              contr_answ=prevForm['contr_answ'].encode('cp1251').decode('latin-1'),
                                              lname=prevForm['lname'].encode('cp1251').decode('latin-1'),
                                              fname=prevForm['fname'].encode('cp1251').decode('latin-1'),
                                              mname=prevForm['mname'].encode('cp1251').decode('latin-1'),
                                              dept_id=prevForm['dept_id'],
                                              title_id=prevForm['title_id'],
                                              title=prevForm['title'].encode('cp1251').decode('latin-1'),
                                              email=prevForm['email'],
                                              phone=prevForm['phone'],
                                              welcome_msg=prevForm['welcome_msg'].encode('cp1251').decode('latin-1'),
                                              exp_date=prevForm['exp_date'],
                                              admin_level=prevForm['admin_level'],
                                              admin=prevForm['admin'],
                                              mgroup_id=prevForm['mgroup_id'],
                                              operator=prevForm['operator'],
                                              state=prevForm['state'],
                                              creator=prevForm['creator'],
                                              passwd=prevForm['passwd'],
                                              )
                        updateUser.save()
                        history = UsersHistory()
                        history.user_id = pk
                        history.date = datetime.now()
                        history.action = "CHDATA"
                        history.creator = request.COOKIES.get('username')
                        history.reason = changes
                        history.ip = get_client_ip(request)
                        history.save()
                        form = userAllForm()
                        infoAboutUser = UsersAll.show_all(UsersAll.objects.filter(login=get_user.login))[0]
                        infoAboutUser["dept_id"] = DeptAll.objects.get(pk=infoAboutUser["dept_id"])
                        infoAboutUser["title_id"] = TitleAll.objects.get(pk=infoAboutUser["title_id"])
                        context = {
                            'get_user': get_user,
                            'userInfo': infoAboutUser,
                            'form': form,
                            'lvl': int(request.COOKIES.get('iqlvl')),
                            'base_template': base_template
                        }
                        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                              template, context)
                else:
                    error = "Імейл не дійсний"
            form.data._mutable = _mutable
            infoAboutUser = UsersAll.show_all(UsersAll.objects.filter(login=get_user.login))[0]
            infoAboutUser["dept_id"] = DeptAll.objects.get(pk=infoAboutUser["dept_id"])
            infoAboutUser["title_id"] = TitleAll.objects.get(pk=infoAboutUser["title_id"])
            context = {
                'get_user': get_user,
                'userInfo': infoAboutUser,
                'form': form,
                'lvl': int(request.COOKIES.get('iqlvl')),
                'info': error,
                'base_template': base_template
            }
            return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                  template, context)
        form = userAllForm()
        context = {
            'get_user': get_user,
            'userInfo': infoAboutUser,
            'form': form,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'info': error,
            'base_template': base_template
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              template, context)

    else:
        return delete_cookies()


def HistoryView(request, pk):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 2:
        template = 'main/all_history.html'
        get_user = UsersHistory.objects.get(pk=pk)
        get_user.date = get_user.date.strftime("%d-%m-%Y")
        if get_user.reason != None:
            get_user.reason = "\t".join(get_user.reason.split("'"))

        context = {
            'get_user': get_user,
            'lvl': int(request.COOKIES.get('iqlvl'))
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              template, context)
    else:
        return delete_cookies()


def mypage(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 1:
        base_template = ""
        if int(request.COOKIES.get('iqlvl')) >= 2:
            base_template = "main/layout.html"
        else:
            base_template = "main/userlayout.html"
        error = ""
        only_view = True
        template = 'main/user_update.html'
        pk = UsersAll.objects.get(login=request.COOKIES.get('username')).user_id
        get_user = UsersAll.objects.get(pk=pk)
        infoAboutUser = UsersAll.show_all(UsersAll.objects.filter(login=get_user.login))[0]
        infoAboutUser["dept_id"] = DeptAll.objects.get(pk=infoAboutUser["dept_id"])
        infoAboutUser["title_id"] = TitleAll.objects.get(pk=infoAboutUser["title_id"])
        infoAboutUser["exp_date"] = infoAboutUser["exp_date"].strftime("%d-%m-%Y")
        form = userAllForm()
        context = {
            'get_user': get_user,
            'userInfo': infoAboutUser,
            'form': form,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'info': error,
            'only_view': only_view,
            'base_template': base_template
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              template, context)

    else:
        return delete_cookies()


def accesstovpn(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 4:
        base_template = "main/layout.html"
        error = ""
        template = 'main/VPN.html'

        form = UsersAccessGroup.objects.all()
        groupVPN = []
        groupNOC = []
        for el in form:
            if str(el.group) == "VPN":
                groupVPN.append(el)
            else:
                groupNOC.append(el)

        groupNOC.reverse()
        groupVPN.reverse()
        groupVPN = groupVPN[:5]
        groupNOC = groupNOC[:5]
        context = {
            'form': form,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'info': error,
            'base_template': base_template,
            'groupVPN': groupVPN,
            'groupNOC': groupNOC,
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              template, context)
    else:
        return delete_cookies()


def addtovpn(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 4:
        users = ""
        error = ""
        info_show = False
        searching_users = []
        btn = False
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["fname"] != "" or form.data["login"] != "" or form.data["document_id"] != ""
                    or form.data["lname"] != "" or form.data["mname"] != "" or form.data["email"] != ""):
                users = UsersAll.search_all(
                    UsersAll.objects.filter(fname__icontains=form.data["fname"].encode('cp1251').decode('latin-1'))
                        .filter(login__icontains=form.data["login"])
                        .filter(document_id__icontains=form.data["document_id"])
                        .filter(lname__icontains=form.data["lname"].encode('cp1251').decode('latin-1'))
                        .filter(mname__icontains=form.data["mname"].encode('cp1251').decode('latin-1'))
                        .filter(email__icontains=form.data["email"]))
                if users != []:
                    if (len(users) > 1):
                        searching_users = []
                        error = "Уточніть запит"
                    else:
                        for i in range(0, len(users)):
                            for el in users[i].keys():
                                if isinstance(users[i][el], str):
                                    users[i][el] = users[i][el].encode('latin-1').decode('cp1251')
                        info_show = True
                        for el in users:
                            el["dept_id"] = DeptAll.objects.get(dept_id=el["dept_id"])
                            searching_users.append(el)
                        try:
                            if UsersAccessGroup.objects.get(
                                    user_id=UsersAll.objects.get(login=searching_users[0]["login"])
                                            .user_id).group_id == 1:
                                btn = True
                        except:
                            pass
                else:
                    error = "За такими данними користувача не знайдено."

                if 'addtovpn' in request.POST:
                    newuserinaccessgroup = UsersAccessGroup()
                    newuserinaccessgroup.user_id = UsersAll.objects.get(login=searching_users[0]["login"]).user_id
                    newuserinaccessgroup.group_id = 1
                    newuserinaccessgroup.save()
                    history = UsersHistory()
                    history.user_id = UsersAll.objects.get(login=searching_users[0]["login"]).user_id
                    history.date = datetime.now()
                    history.action = "CHDATA"
                    history.reason = "Changed VPN group"
                    history.creator = request.COOKIES.get('username')
                    history.ip = get_client_ip(request)
                    history.save()
                    btn = True
                data = {
                    'form': form,
                    'lvl': int(request.COOKIES.get('iqlvl')),
                    'info': searching_users,
                    'error': error,
                    'show': info_show,
                    'btn': btn,
                    'vpn': 'VPN'
                }
                return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                      'main/addtoVPN.html', data)
            else:
                error = "Уведіть хоча б один із пунктів для пошуку"

        form = userAllForm()
        data = {
            'form': form,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'info': users,
            'error': error,
            'show': info_show,
            'btn': btn,
            'vpn':'VPN'
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/addtoVPN.html', data)
    else:
        return delete_cookies()


def addtovpn_noc(request):
    if check_cookies(request.COOKIES.get('username'), request.COOKIES.get('login_status')) \
            and int(request.COOKIES.get('iqlvl')) >= 5:
        users = ""
        error = ""
        info_show = False
        searching_users = []
        btn = False
        if request.method == "POST":
            form = userAllForm(request.POST)
            if (form.data["fname"] != "" or form.data["login"] != "" or form.data["document_id"] != ""
                    or form.data["lname"] != "" or form.data["mname"] != "" or form.data["email"] != ""):
                users = UsersAll.search_all(
                    UsersAll.objects.filter(fname__icontains=form.data["fname"].encode('cp1251').decode('latin-1'))
                        .filter(login__icontains=form.data["login"])
                        .filter(document_id__icontains=form.data["document_id"])
                        .filter(lname__icontains=form.data["lname"].encode('cp1251').decode('latin-1'))
                        .filter(mname__icontains=form.data["mname"].encode('cp1251').decode('latin-1'))
                        .filter(email__icontains=form.data["email"]))
                if users != []:
                    if (len(users) > 1):
                        searching_users = []
                        error = "Уточніть запит"
                    else:
                        for i in range(0, len(users)):
                            for el in users[i].keys():
                                if isinstance(users[i][el], str):
                                    users[i][el] = users[i][el].encode('latin-1').decode('cp1251')
                        info_show = True
                        for el in users:
                            el["dept_id"] = DeptAll.objects.get(dept_id=el["dept_id"])
                            searching_users.append(el)
                        try:
                            if UsersAccessGroup.objects.get(user_id=UsersAll.objects.get(
                                    login=searching_users[0]["login"]).user_id).group_id == 2:
                                btn = True
                        except:
                            pass
                else:
                    error = "За такими данними користувача не знайдено."

                if 'addtovpn' in request.POST:
                    newuserinaccessgroup = UsersAccessGroup()

                    newuserinaccessgroup.user_id = UsersAll.objects.get(login=searching_users[0]["login"]).user_id
                    newuserinaccessgroup.group_id = 2
                    newuserinaccessgroup.save()
                    history = UsersHistory()
                    history.user_id = UsersAll.objects.get(login=searching_users[0]["login"]).user_id
                    history.date = datetime.now()
                    history.action = "CHDATA"
                    history.reason = "Changed VPN group"
                    history.creator = request.COOKIES.get('username')
                    history.ip = get_client_ip(request)
                    history.save()
                    btn = True
                data = {
                    'form': form,
                    'info': searching_users,
                    'lvl': int(request.COOKIES.get('iqlvl')),
                    'error': error,
                    'show': info_show,
                    'btn': btn,
                    'vpn': 'VPN-NOC'
                }
                return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                                      'main/addtoVPN.html', data)
            else:
                error = "Уведіть хоча б один із пунктів для пошуку"

        form = userAllForm()
        data = {
            'form': form,
            'info': users,
            'lvl': int(request.COOKIES.get('iqlvl')),
            'error': error,
            'show': info_show,
            'btn': btn,
            'vpn': 'VPN-NOC'
        }
        return create_cookies(request, request.COOKIES.get('iqlvl'), request.COOKIES.get('username'),
                              'main/addtoVPN.html', data)
    else:
        return delete_cookies()


def recoverypass(request, code):
    success = ""
    if request.method == "POST":
        form = change_passForm(request.POST)
        users = RestorePassword.objects.get(temporary_pass=code)
        if users.exp_date > datetime.now():
            if (form.data["password"] == form.data["repassword"]):
                if (len(form.data["password"]) >= 8):
                    password = form.data["password"]
                    password = hashMDPass(password)
                    user = UsersAll(user_id=users.user)
                    user.passwd = password
                    history = UsersHistory()
                    history.user_id = users.user
                    history.date = datetime.now()
                    history.action = "CHPASS"
                    history.creator = UsersAll.objects.get(user_id=users.user).login
                    history.ip = get_client_ip(request)
                    history.reason = "Recover password"
                    history.save()
                    user.save(update_fields=['passwd'])
                    return redirect('login')
                else:
                    success = "Мінімальна довжина паролю 8 символів."
            else:
                success = "Паролі не співпадають"
        else:
            success = "Час зміни паролю сплив"

    form = change_passForm()
    data = {
        'form': form,
        "success": success
    }
    return render(request, 'main/recovery.html', data)
