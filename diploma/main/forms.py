from .models import users_all, faculty_all
from django.forms import ModelForm, TextInput, ChoiceField
from django import forms


class userAllForm(ModelForm):
    use_required_attribute = False

    class Meta:
        model = users_all
        fields = [
            "dept_id", "state", "login", "passwd",
            "fname", "lname", "mname", "contr_quest", "contr_answ",
            "title", "email", "phone", "exp_date", "welcome_msg",
            "admin", "document_id", "creator",
            "operator", "mgroup_id", "title_id", "admin_level"
        ]
        widgets = {
            "exp_date": TextInput(attrs={
                'type':'text',
                'class':'form-control',
                'id':'datepicker-example'
            }),
            "login" : TextInput(attrs={
                'required': False,
                'id': "crit"
            }),
            "document_id": TextInput(attrs={
                'required': False,
                'id': "crit"
            }),
            "passwd": TextInput(attrs={
                'required': False,
                'type': 'password',
                'id': "crit"
            }),
            "lname": TextInput(attrs={
                'required':False,
                'id': "crit"
            }),
            "fname": TextInput(attrs={
                'required':False,
                'id': "crit"
            }),
            "mname": TextInput(attrs={
                'required':False,
                'id': "crit"
            }),



            "contr_quest": TextInput(attrs={
                'required':False
            }),
            "contr_answ": TextInput(attrs={
                'required':False
            }),
            "title": TextInput(attrs={
                'required':False
            }),
            "welcome_msg": TextInput(attrs={
                'required': False
            }),
            "phone": TextInput(attrs={
                'required': False
            }),
            "email": TextInput(attrs={
                'required': False,
                'id': "email"
            })
        }


class change_passForm(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    repassword = forms.CharField(widget=forms.PasswordInput())




class faculty_allForm(ModelForm):
    class Meta:
        facultets = faculty_all.objects.all()
        CHOICES = []
        for el in facultets:
            CHOICES.append([el.faculty,el.faculty])

        fields = ChoiceField(choices=CHOICES)

