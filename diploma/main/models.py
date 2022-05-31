from django.db import models


# Create your models here.

class access_group(models.Model):
    id = models.AutoField(primary_key=True, db_column="group_id")
    name = models.CharField("name", max_length=50)
    description = models.CharField("description", max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Access Group"
        verbose_name_plural = "Access Group"


class dept_all(models.Model):
    id = models.AutoField(primary_key=True, db_column="dept_id")
    dept_ename = models.CharField("dept_ename", max_length=64)
    dept_uname = models.CharField("dept_uname", max_length=64)
    copymail = models.CharField("copymail", max_length=50, blank=True)

    def __str__(self):
        return self.dept_uname

    class Meta:
        verbose_name = "Dept all"
        verbose_name_plural = "Dept all"


class faculty_all(models.Model):
    id = models.AutoField(primary_key=True, db_column="faculty_id")
    faculty = models.CharField("faculty", max_length=30)
    dept_id = models.IntegerField("dept_id")

    def __str__(self):
        return self.faculty

    class Meta:
        verbose_name = "Faculty All"
        verbose_name_plural = "Faculty All"


class title_all(models.Model):
    id = models.AutoField(primary_key=True, db_column="title_id")
    title_uname = models.CharField("title_uname", max_length=30)
    title_ename = models.CharField("title_ename", max_length=30)

    def __str__(self):
        return self.title_uname

    class Meta:
        verbose_name = "Title All"
        verbose_name_plural = "Title All"


class users_access_group(models.Model):
    id = models.AutoField(primary_key=True, db_column="user_id")
    group_id = models.IntegerField("group_id")
    desc = models.TextField("desc")

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = "users_access_group"
        verbose_name_plural = "users_access_group"


class users_history(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    date = models.DateTimeField()
    actions = [
        ('CREATION', 'CREATION'),
        ('WARNING', 'WARNING'),
        ('CLOSING', 'CLOSING'),
        ('ACTIVATION', 'ACTIVATION'),
        ('CHPASS', 'CHPASS'),
        ('EXT_EXPIRE', 'EXT_EXPIRE'),
        ('CHDATA', 'CHDATA')
    ]
    action = models.CharField('Action', max_length=20, choices=actions, default='CREATION', blank=True)
    creator = models.CharField("creator", max_length=16, blank=True)
    reason = models.TextField("reason", blank=True)
    ip = models.TextField("ip", max_length=15, blank=True)

    def history_user(self):
        user = []
        for i in self:
            user.append({
                "id": i.id,
                "date": i.date,
                "action": i.action,
                "creator": i.creator,
                "reason": i.reason,
                "state": i.state,
                "ip": i.ip,
                "passwd": i.passwd
            })
        #user = self
        return user

    class Meta:
        verbose_name = "users history"
        verbose_name_plural = "users history"


class users_all(models.Model):
    id = models.AutoField(primary_key=True, db_column="user_id")
    dept_id = models.ForeignKey(dept_all, default=0, on_delete=models.CASCADE)
    states = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED')
    ]
    state = models.CharField('state', max_length=10, choices=states, default='OPEN', blank=True)
    login = models.CharField("login", max_length=16)

    passwd = models.CharField("passwd", max_length=100)

    fname = models.CharField("fname", max_length=50)

    lname = models.CharField("lname", max_length=50)

    mname = models.CharField("mname", max_length=50)

    contr_quest = models.CharField("contr_quest", default="-", max_length=255, blank=True)

    contr_answ = models.CharField("contr_answ", default="-", max_length=255, blank=True)

    title = models.CharField("title", default="-", max_length=30, blank=True)

    email = models.CharField("email", max_length=50, blank=True)

    phone = models.CharField("phone", default="+380", max_length=30, blank=True)

    exp_date = models.DateTimeField("exp_date")

    welcome_msg = models.CharField("welcome_msg", default="-", max_length=255, blank=True)

    admins = [
        ("n", "n"),
        ("y", "y")
    ]
    admin = models.CharField('admin', max_length=2, choices=admins, default='n', blank=True)
    document_id = models.CharField("document_id", max_length=16)
    creator = models.CharField("creator", default="name", max_length=16, blank=True)
    operators = [
        ("n", "n"),
        ("y", "y")
    ]
    operator = models.CharField('operator', max_length=2, choices=operators, default='n', blank=True)
    mgroup_id = models.ForeignKey(access_group, default=0, on_delete=models.CASCADE)
    title_id = models.ForeignKey(title_all, default=1, on_delete=models.CASCADE)
    lvl = [
        ("0", 0),
        ('1', 1),
        ('2', 2),
        ('3', 3)
    ]
    admin_level = models.IntegerField("admin_level", default="1", blank=True)

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
                "id": i.id,
                "passwd": i.passwd,
                "email": i.email,
                "document_id": i.document_id
            })
        #user = self
        return user

    def adminRole(self):
        if(self == '1'):
            return 1
        elif(self == '2'):
            return 2
        elif (self == '3'):
            return 3

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "users_all"
        verbose_name_plural = "users_all"
