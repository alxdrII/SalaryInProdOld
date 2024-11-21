from datetime import time
from django.utils import timezone
from django.db import models


# Create your models here.
class CreatedProducts(models.Model):
    """
    Документ выработки продукции.
    Шапка документа о выпуске продукции бригадой сотрудников, содержит общий процент выработки

    """

    doc_data = models.DateField(default=timezone.now(), verbose_name='Дата')
    doc_number = models.PositiveSmallIntegerField(unique_for_year='doc_data', null=False, verbose_name='Номер')
    percent = models.DecimalField(max_digits=8, decimal_places=5, verbose_name='Процент выработки') # рассчитывается
    description = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name_plural = 'Документы выработки'
        verbose_name = 'Документ выработки'
        ordering = ['doc_data']

    def __str__(self):
        return f'Выработка № {self.doc_number} от {self.doc_data}'


class Product(models.Model):
    """
    Изделия.
    Список всей продукции, которую производим.

    """

    code = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    quota = models.PositiveSmallIntegerField(verbose_name='Норма выработки')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Изделия'
        verbose_name = 'Изделие'
        ordering = ['code']

    def __str__(self):
        return self.code


class Production(models.Model):
    """
    Выработка
    Табличная часть документа выработки продукции. Содержит список и количество продукции,
    выработанной отчетной сменой

    """

    doc = models.ForeignKey(CreatedProducts, on_delete=models.CASCADE, verbose_name='Документ')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, verbose_name='Изделие')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    percent = models.DecimalField(max_digits=8, decimal_places=5, verbose_name='Процент от нормы')  # Процент от нормы (рассчитывается)

    class Meta:
        verbose_name_plural = 'Выработки'
        verbose_name = 'Выработка'
        ordering = ['doc']

    def __str__(self):
        # result = self.quantity / self.product.quota * 100
        return f'{self.product.code}'


class Employee(models.Model):
    """
    Сотрудники.
    Список всех сотрудников работающих или работавших на производственного предприятии

    """

    STATUS = ((True, 'Уволен'), (False, 'Сотрудник'))

    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    hired = models.DateField(default=timezone.now(), verbose_name='Устроен')
    dismissed = models.BooleanField(choices=STATUS, default=False, verbose_name='Статус')

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'
        ordering = ['fullname']

    def __str__(self):
        return self.fullname


class Brigade(models.Model):
    """
    Бригада.
    Табличная часть документа выработки продукции. Содержит список сотрудников,
    участвовавших в производстве изделий за смену и время, которе они затратили

    """

    doc = models.ForeignKey(CreatedProducts, on_delete=models.CASCADE, verbose_name='Документ')
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT, verbose_name='Сотрудник')
    working = models.TimeField(default=time(12, 0, 0), verbose_name='Отработанное время')

    class Meta:
        verbose_name_plural = 'Бригады'
        verbose_name = 'Бригада'
        ordering = ['doc']

    def __str__(self):
        return str(self.employee)
