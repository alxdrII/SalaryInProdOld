from datetime import time, timedelta
from django.utils import timezone
from django.db import models


class CreatedProducts(models.Model):
    """ Документ выработки продукции.

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


class Drawing(models.Model):
    """
    Рисунок наносимый на форму изделия
    """

    name = models.CharField(max_length=25, unique=True, verbose_name='Рисунок')

    class Meta:
        verbose_name_plural = 'Рисунки'
        verbose_name = 'Рисунок'
        ordering = ['name']

    def __str__(self):
        return self.name


class Shape(models.Model):
    """
    Форма изделия
    """

    name = models.CharField(max_length=25, unique=True, verbose_name='Форма')

    class Meta:
        verbose_name_plural = 'Формы'
        verbose_name = 'Форма'
        ordering = ['name']

    def __str__(self):
        return self.name


class Workshop(models.Model):
    """
    Цех.

    Место производства
    """

    name = models.CharField(max_length=25, unique=True, verbose_name='Цех')
    # work_drt = models.TimeField(default=time(12, 0, 0), verbose_name='Продолжительность смены')
    work_drt = models.DurationField(default=timedelta(hours=12), verbose_name='Продолжительность смены')
    repair_drt = models.DurationField(blank=True, verbose_name='Продолжительность ремонта')
    reboot_drt = models.DurationField(blank=True, verbose_name='Продолжительность перезагрузки')
    process_drt = models.DurationField(blank=True, verbose_name='Продолжительность обработки')
    power = models.PositiveSmallIntegerField(blank=True, verbose_name='Мощность')
    correction = models.DecimalField(max_digits=8, decimal_places=5, verbose_name='Общая коррекция')
    machines_num = models.PositiveSmallIntegerField(verbose_name='Количество станков')

    class Meta:
        verbose_name_plural = 'Цеха'
        verbose_name = 'Цех'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Изделия.

    Список производимой продукции
    """

    code = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    quota = models.PositiveSmallIntegerField(verbose_name='Норма выработки')
    description = models.TextField(blank=True, verbose_name='Описание')

    power = models.PositiveSmallIntegerField(blank=True, verbose_name='Мощность')
    process_drt = models.DurationField(blank=True, verbose_name='Продолжительность обработки')
    complexity = models.DecimalField(max_digits=8, decimal_places=5, verbose_name='Сложность изготовления')
    limit = models.PositiveSmallIntegerField(blank=True, verbose_name='Предел')

    workshop = models.ForeignKey(Workshop, on_delete=models.RESTRICT, verbose_name='Цех')
    shape = models.ForeignKey(Shape, on_delete=models.RESTRICT, verbose_name='Форма')
    drawing = models.ForeignKey(Drawing, on_delete=models.RESTRICT, verbose_name='Рисунок')

    class Meta:
        verbose_name_plural = 'Изделия'
        verbose_name = 'Изделие'
        ordering = ['code']

    def __str__(self):
        return self.code


class Production(models.Model):
    """
    Выработка

    Табличная часть документа выработки продукции.
    Содержит список и количество продукции, выработанной отчетной сменой
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

    Список сотрудников производственного предприятии
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

    Табличная часть документа выработки продукции.
    Содержит список сотрудников, участвовавших в производстве изделий за смену
    и время, которе они затратили
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

'''
class Specification(models.Model):
    """ Спецификация продукции """
    
    workshop = models.ForeignKey(Workshop, on_delete=models.RESTRICT, verbose_name='Цех')
    shape = models.ForeignKey(Shape, on_delete=models.RESTRICT, verbose_name='Форма')
    drawing = models.ForeignKey(Drawing, on_delete=models.RESTRICT, verbose_name='Рисунок')
    power = models.PositiveSmallIntegerField(blank=True, verbose_name='Мощность')
    proces_drt = models.TimeField(blank=True, verbose_name='Продолжительность обработки')
    complexity = models.DecimalField(max_digits=8, decimal_places=5, verbose_name='Сложность изготовления')
    limit = models.PositiveSmallIntegerField(blank=True, verbose_name='Предел')
    
    class Meta:
        verbose_name_plural = 'Спецификации'
        verbose_name = 'Спецификация'
        ordering = ['name']
'''