from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

STATUSES = (
    (1, 'Nieprzydzielone'),
    (2, 'W toku'),
    (3, 'Zakończone'),
)


class Workshop(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nazwa')
    address = models.CharField(max_length=255, verbose_name='Adres')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Position(models.Model):
    number = models.IntegerField(verbose_name='Numer stanowiska')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('number', 'workshop')


    def __str__(self):
        return f'{self.pk}'

class Mechanic(models.Model):
    name = models.CharField(max_length=255, verbose_name='Imię')
    surname = models.CharField(max_length=255, verbose_name='Nazwisko')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    default_position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Stanowisko')

    @property
    def mechanic_name(self):
        return "{} {}".format(self.name, self.surname)

    @property
    def orders_all(self):
        return self.order_set.all()

    @property
    def orders_time(self):
        return self.order_set.all().aggregate(Sum('estimated_working_time'))['estimated_working_time__sum']

    @property
    def orders_status(self):
        return self.order_set.get(order_status=1).number

        # return self.order_set.get(order_status=2).number

    def __str__(self):
        return f'{self.mechanic_name}'


class Order(models.Model):
    description = models.TextField(verbose_name='Opis')
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True, verbose_name='Data przyjęcia zlecenia')
    start_date = models.DateField(blank=True, null=True, verbose_name='Data rozpoczęcia pracy')
    end_date = models.DateField(blank=True, null=True, verbose_name='Data zakończenia pracy')
    estimated_working_time = models.IntegerField(verbose_name='Przewidywany czas pracy ')
    order_status = models.IntegerField(choices=STATUSES, verbose_name='Status', default=1)
    number = models.IntegerField(verbose_name='Numer zlecenia')

    class Meta:
        ordering=['date_added']
