from .models import UsersAll, FacultyAll, AccessGroup, UsersAccessGroup, TitleAll, DeptAll
from django.forms import ModelForm, TextInput, ChoiceField
from django import forms


class userAllForm(forms.Form):
    use_required_attribute = False
    dept_id = forms.ModelChoiceField(queryset=DeptAll.objects.all())
    states = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED')
    ]
    state = forms.CharField(widget=forms.Select(choices=states))
    login = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={
            'required': False,
            'id': "crit"
        }))
    passwd = forms.CharField(max_length=40, widget=forms.PasswordInput)
    fname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'required': False,
            'id': "crit"
        }))
    lname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'required': False,
            'id': "crit"
        }))
    mname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'required': False,
            'id': "crit"
        }))
    contr_quest = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'required': False
        }))
    contr_answ = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'required': False
        }))
    title = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'required': False
        }))
    email = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'required': False,
            'id': "email"
        }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'required': False
        }))
    exp_date = forms.DateTimeField(widget=forms.PasswordInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'id': 'datepicker-example'
        }))
    welcome_msg = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'required': False
        }))
    admins = [
        ("n", "n"),
        ("y", "y")
    ]
    admin = forms.CharField(widget=forms.Select(choices=admins))
    document_id = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={
            'required': False,
            'id': "crit"
        }))
    creator = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={
            'required': False
        }))
    operators = [
        ("n", "n"),
        ("y", "y")
    ]
    operator = forms.CharField(widget=forms.Select(choices=operators))
    mgroup_id = forms.IntegerField()
    title_id = forms.ModelChoiceField(queryset=TitleAll.objects.all())
    admin_level = forms.IntegerField()

class change_passForm(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    repassword = forms.CharField(widget=forms.PasswordInput())


class remindpass(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    document_id = forms.CharField(label='Login', max_length=100, widget=forms.TextInput(attrs={
        'id': 'document_id',
        'readonly': 'readonly',
        'type': 'password'
    }))


class FacultyAllForm(ModelForm):
    class Meta:
        facultets = FacultyAll.objects.all()
        CHOICES = []
        for el in facultets:
            CHOICES.append([el.faculty, el.faculty])

        fields = ChoiceField(choices=CHOICES)


class usersupdateform(forms.ModelForm):
    class Meta:
        model = UsersAll
        fields = '__all__'


class Users_access_group_form(ModelForm):
    class Meta:
        model = UsersAccessGroup
        fields = ['user', 'group', 'desc']


