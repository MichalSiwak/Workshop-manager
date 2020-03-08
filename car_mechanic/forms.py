from django import forms
from django.core.exceptions import ValidationError
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=120)
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=120)
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)
    rep_password = forms.CharField(label='Powtórz hasło', max_length=120, widget=forms.PasswordInput)
    first_name = forms.CharField(label='Imię', max_length=120)
    last_name = forms.CharField(label='Nazwisko', max_length=120)
    email = forms.EmailField(label="E-mail")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        user = User.objects.filter(username=username)  # User.objects.filter - tworzy tablice.
        if len(user) != 0:
            raise ValidationError('Podany użytkownik już istnieje')
        password = cleaned_data.get('password')
        rep_password = cleaned_data.get('rep_password')
        if password != rep_password:
            raise forms.ValidationError('Hasło i powtórzone hasło się nie zgadzają')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'e-mail'
        }


class AddWorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['name', 'address']


class AddMechanicForm(forms.ModelForm):
    default_position_id = forms.ChoiceField(choices=[], label='Nr stanowiska')

    def __init__(self, user_id, *args, **kwargs):
        super(AddMechanicForm, self).__init__(*args, **kwargs)
        workshops = Workshop.objects.filter(user_id=user_id)
        workshop = workshops.get().pk
        self.fields['default_position_id'].choices = [(position.pk, position.number) for position in Position.objects.filter(workshop_id=workshop)]

    class Meta:
        model = Mechanic
        fields = ['name', 'surname']


class EditMechanicForm(forms.ModelForm):

    def __init__(self, user_id, *args, **kwargs):
        super(EditMechanicForm, self).__init__(*args, **kwargs)
        workshops = Workshop.objects.filter(user_id=user_id)
        workshop = workshops.get().pk
        self.fields['default_position'].choices = \
            [(position.pk, position.number) for position in Position.objects.filter(workshop_id=workshop)]

    class Meta:
        model = Mechanic
        fields = ['name', 'surname', 'default_position']


class AddPositionForm(forms.Form):
    number = forms.IntegerField()


# class OrderListForm(forms.Form):
#     orders = Order.objects.all()
#     orders_list =[(order.pk, order.pk) for order in orders]
#     order_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     mechanics = Mechanic.objects.all()
#     mechanic_list = [(mechanic.pk, mechanic.pk) for mechanic in mechanics]
#     mechanic_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     date_added = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     start_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     end_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     order_status = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))


class AddNewPositionForm(forms.Form):
    number = forms.IntegerField()


class AddOrderForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label='Opis')
    estimated_working_time = forms.IntegerField(label='Przewidywany czas pracy')
    number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Numer zamówienia')



class EditOrderForm(forms.Form):
    number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Numer zamówienia')
    description = forms.CharField(widget=forms.Textarea, label='Opis')
    mechanics = Mechanic.objects.all()
    mechanic_list = [(mechanic.pk, mechanic) for mechanic in mechanics]
    mechanic = forms.ChoiceField(choices=mechanic_list, label='Mechanik')
    date_added = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Data przyjęcia')
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Data rozpoczęcia pracy')
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Data zakonczenia pracy')
    estimated_working_time = forms.IntegerField(label='Przewidywany czas pracy')
    order_status = forms.ChoiceField(choices=STATUSES, label='Status zlecenia')

    def __init__(self, user_id, *args, **kwargs):
        super(EditOrderForm, self).__init__(*args, **kwargs)
        workshops = Workshop.objects.filter(user_id=user_id)
        workshop = workshops.get().pk
        self.fields['mechanic'].choices = \
            [(mechanic.pk, mechanic.name) for mechanic in Mechanic.objects.filter(workshop_id=workshop)]
