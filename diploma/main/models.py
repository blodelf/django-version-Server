from django.db import models


class AccessGroup(models.Model):
    group_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'access_group'

    def __str__(self):
        return self.name


class DeptAll(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_ename = models.CharField(unique=True, max_length=64)
    dept_uname = models.CharField(unique=True, max_length=64)
    copymail = models.CharField(max_length=50)

    class Meta:
        db_table = 'dept_all'

    def __str__(self):
        return self.dept_ename


class FacultyAll(models.Model):
    faculty_id = models.PositiveIntegerField(primary_key=True)
    faculty = models.CharField(max_length=30, blank=True, null=True)
    dept_id = models.IntegerField()

    class Meta:
        db_table = 'faculty_all'

    def __str__(self):
        return self.faculty


class TitleAll(models.Model):
    title_id = models.AutoField(primary_key=True)
    title_uname = models.CharField(unique=True, max_length=30)
    title_ename = models.CharField(unique=True, max_length=30)

    class Meta:
        db_table = 'title_all'

    def __str__(self):
        return self.title_ename


class UsersAccessGroup(models.Model):
    user = models.OneToOneField('UsersAll', models.DO_NOTHING, primary_key=True)

    group = models.ForeignKey(AccessGroup, models.DO_NOTHING)

    desc = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'users_access_group'

        unique_together = (('user', 'group'),)

    def __str__(self):
        return str(self.group)


class UsersAll(models.Model):
    user_id = models.AutoField(primary_key=True)

    dept_id = models.PositiveIntegerField()

    state = models.CharField(max_length=6)

    login = models.CharField(unique=True, max_length=16)

    passwd = models.CharField(max_length=40)

    fname = models.CharField(max_length=50)

    lname = models.CharField(max_length=50)

    mname = models.CharField(max_length=50)

    contr_quest = models.CharField(max_length=255)

    contr_answ = models.CharField(max_length=255)

    title = models.CharField(max_length=30)

    email = models.CharField(max_length=50)

    phone = models.CharField(max_length=20, blank=True, null=True)

    exp_date = models.DateTimeField(blank=True, null=True)

    welcome_msg = models.CharField(max_length=255, blank=True, null=True)

    admin = models.CharField(max_length=1)

    document_id = models.CharField(max_length=16)

    creator = models.CharField(max_length=16)

    operator = models.CharField(max_length=1)

    mgroup_id = models.IntegerField()

    title_id = models.PositiveIntegerField()

    admin_level = models.PositiveIntegerField()

    def search_all(self) -> object:
        user = []
        for i in self:
            user.append({
                "login": i.login,
                "fname": i.fname,
                "mname": i.mname,
                "lname": i.lname,
                "dept_id": i.dept_id,
                "state": i.state,
                "id": i.user_id,
                "passwd": i.passwd,
                "email": i.email,
                "document_id": i.document_id,
                "exp_date": i.exp_date.date().strftime("%d-%m-%Y")
            })
        # user = self
        return user

    def show_all(self) -> object:
        user = []
        for i in self:
            if i.welcome_msg == None:
                i.welcome_msg = ""
            user.append({
                "dept_id": i.dept_id,
                "state": i.state,
                "login": i.login,
                "passwd": i.passwd,
                "fname": i.fname.encode('latin-1').decode('cp1251'),
                "mname": i.mname.encode('latin-1').decode('cp1251'),
                "lname": i.lname.encode('latin-1').decode('cp1251'),
                "contr_quest": i.contr_quest.encode('latin-1').decode('cp1251'),
                "contr_answ": i.contr_answ.encode('latin-1').decode('cp1251'),
                "title": i.title.encode('latin-1').decode('cp1251'),
                "email": i.email,
                "phone": i.phone,
                "exp_date": i.exp_date,
                "welcome_msg": i.welcome_msg.encode('latin-1', errors='ignore').decode('cp1251', errors='ignore'),
                "admin": i.admin,
                "document_id": i.document_id,
                "creator": i.creator,
                "operator": i.operator,
                "mgroup_id": i.mgroup_id,
                "title_id": i.title_id,
                "admin_level": i.admin_level
            })
        # user = self
        return user

    def adminRole(self):
        if (self == '1' or self == ''):
            return 1
        elif (self == '4'):
            return 4
        else:
            return 2

    class Meta:
        db_table = 'users_all'

    def __str__(self):
        return self.login


class UsersHistory(models.Model):
    user_id = models.PositiveIntegerField()

    date = models.DateTimeField()

    action = models.CharField(max_length=10)

    creator = models.CharField(max_length=16)

    reason = models.TextField(blank=True, null=True)

    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'users_history'


class RestorePassword(models.Model):
    record_id = models.AutoField(primary_key=True)
    user = models.PositiveIntegerField()
    exp_date = models.DateTimeField()
    created_date = models.DateTimeField()
    ip = models.CharField(max_length=15, blank=True, null=True)
    temporary_pass = models.CharField(max_length=40)

    class Meta:
        db_table = 'restore_password'
