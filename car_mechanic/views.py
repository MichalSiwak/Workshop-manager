from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from car_mechanic.forms import *
from django.db import transaction



### Login and logout ###

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(** form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Błędny login lub hasło')
                return render(request, 'login.html', {'form': form})
        else:
            messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')
            return redirect('index')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


### start and home page ###

class StartPage(View):
    def get(self, request):
        return render(request, 'index.html')


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        worksop = Workshop.objects.get(user_id=user.id)
        orders = Order.objects.filter(user_id=user.id)
        orders_status = len(orders.filter(mechanic_id=None))
        mechanics = Mechanic.objects.filter(workshop_id=worksop.pk)
        return render(request, 'home.html', {'worksop': worksop, 'user': user,
                      'mechanics': mechanics, 'orders_status': orders_status})

class ContactView(View):
    def get(self, request):
        return HttpResponse('Strona w budowie')


class AboutrView(View):
    def get(self, request):
        return HttpResponse('Strona w budowie')


###User###

class AddUserView(View):
    def get(self, request):
        user_form = AddUserForm()
        workshop_form = AddWorkshopForm()
        return render(request, 'register.html', {'user_form': user_form, 'workshop_form':workshop_form})

    @transaction.atomic
    def post(self, request):
        form = AddUserForm(request.POST)
        if not form.is_valid():
            return redirect('/register')
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            messages.error(request, 'Login zajęty. Wybierz inny.')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                        last_name=last_name)
        user.save()
        name = request.POST.get("name")
        address = request.POST.get("address")
        Workshop.objects.create(name=name, address=address, user_id=user.id)
        messages.info(request, 'Dodano nowego użytkwnika.')
        return redirect('login')


class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditUserForm(initial={"first_name": request.user.first_name,
                                        "last_name": request.user.last_name,
                                        "email": request.user.email})
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = EditUserForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')
        user = request.user
        user_id = user.id
        User.objects.filter(pk=user_id).update(**form.cleaned_data)
        messages.info(request, 'Dane zmenione poprawnie')
        return render(request, 'form.html', {'form': form})


### order ##

class AddOrderView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_id = user.id
        order = Order.objects.filter(user_id=user_id)

        # AutoField
        if len(order) == 0:
            form = AddOrderForm(initial={"number": 1})
            return render(request, 'form.html', {'form': form})
        order_number = order.last().number
        form = AddOrderForm(initial={"number": order_number + 1})
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddOrderForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')
        user = request.user
        user_id = user.id
        Order.objects.create(**form.cleaned_data, user_id=user_id)
        messages.info(request, 'Zamowienie dodane')
        return redirect('home')


class EditOrderView(LoginRequiredMixin, View):
    def get(self, request, number):
        user = request.user
        orders = Order.objects.filter(user_id=user.id)
        order = orders.get(number=number)
        user = request.user
        user_id = user.id
        form = EditOrderForm(user_id, initial={"date_added": order.date_added, "number": order.number, "description": order.description,
        "mechanic": order.mechanic, "start_date": order.start_date,
        "end_date": order.end_date, "estimated_working_time": order.estimated_working_time,
        "order_status": order.order_status})
        return render(request, 'form.html', {'form': form})

    def post(self, request, number):
        user = request.user
        user_id = user.id
        form = EditOrderForm(user_id, request.POST)
        if not form.is_valid():
            messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')
            return redirect('home')
        # user = request.user
        Order.objects.filter(user_id=user.id, number=number).update(** form.cleaned_data)
        messages.info(request, 'Zapisano zmiany')
        return redirect('home')


class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user_id=user.id)
        paginator = Paginator(orders, 5)
        page = request.GET.get('page')
        orders = paginator.get_page(page)
        return render(request, 'order_list.html', {'orders': orders})


### Workshop ###

class EditWorkshopView(View):
    def get(self, request):
            user = request.user
            workshop = Workshop.objects.get(user_id=user.id)
            positions = len(Position.objects.filter(workshop_id=workshop.pk))
            mechaniks = Mechanic.objects.filter(workshop_id=workshop)
            work = AddWorkshopForm(initial={'name': workshop.name, 'address': workshop.address})
            return render(request, 'work_form.html', {'work': work, 'mechaniks': mechaniks,
                                                      'positions': positions})

    def post(self, request):
        form = AddWorkshopForm(request.POST)
        user = request.user
        user_id = user.id
        workshop = Workshop.objects.get(user_id=user_id)
        workshop = workshop.pk
        positions = Position.objects.filter(workshop_id=workshop)

        if request.POST.get("edit"):
            if not form.is_valid():
                messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')
            Workshop.objects.filter(user_id=user.id).update(** form.cleaned_data)
        if len(positions) == 0:
            Position.objects.create(number=1, workshop_id=workshop)
        elif request.POST.get("add"):
            last_position = positions.last().number
            number = last_position + 1
            Position.objects.create(number=number, workshop_id=workshop)
            messages.info(request, 'Dodano nowe stanowisko')
            return redirect('edit_workshop')
        if request.POST.get("delete"):
            last_position = positions.last().number
            Position.objects.filter(number=last_position, workshop_id=workshop).delete()
            messages.info(request, 'Usunięto stanowisko')
            return redirect('edit_workshop')
        messages.info(request, 'Zmieniono informację o warsztacie')
        return redirect('edit_workshop')


class AddMechanicView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_id = user.id
        form = AddMechanicForm(user_id)
        return render(request, 'add_mechanic.html', {"form": form})

    def post(self, request):
        user = request.user
        user_id = user.id
        form = AddMechanicForm(user_id, request.POST)
        if not form.is_valid():
            messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')
        workshop = Workshop.objects.get(user_id=user_id)
        Mechanic.objects.create(** form.cleaned_data, workshop_id=workshop.pk)
        messages.info(request, 'Dano parcownika')
        return redirect('new_mechanic')


class EditMechanicView(LoginRequiredMixin, View):
    def get(self, request, mechanic_id):
        mechanic = Mechanic.objects.get(pk=mechanic_id)
        user = request.user
        user_id = user.id
        form = EditMechanicForm(user_id,
            initial={'name': mechanic.name, 'surname': mechanic.surname,'default_position': mechanic.default_position})
        return render(request, 'edit_mechanic.html', {'form': form})

    def post(self, request, mechanic_id):
        user = request.user
        user_id = user.id
        form = EditMechanicForm(user_id, request.POST)
        if not form.is_valid():
            messages.error(request, 'Nastąpił błąd. Skontaktuj sie z nami!!!')

        if request.POST.get("edit"):
            Mechanic.objects.filter(pk=mechanic_id).update(** form.cleaned_data)
            messages.info(request, 'Zapisano zmiany')
            return redirect('edit_workshop')

        if request.POST.get("delete"):
            Mechanic.objects.filter(pk=mechanic_id).delete()
            messages.info(request, 'Usunięto')
            return redirect('edit_workshop')