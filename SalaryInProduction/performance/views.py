from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.utils.timezone import localdate
from django.db.models import Sum, Avg
from .models import CreatedProducts, Production, Brigade, Product, Employee


def recalc_percent_doc(doc_id):
    """
    Расчет процента выработки документа.
    :param doc_id: id документа

    """
    total_percent = Production.objects.filter(doc_id=doc_id).aggregate(Sum('percent'))['percent__sum']
    CreatedProducts.objects.filter(id=doc_id).update(percent=total_percent)


def array_for_date_selection():
    """
    Функция возвращает кортеж списков названий месяцев и числа последних 5 лет
    :return: (years, mounts, year, month)
    """
    month = localdate().month
    year = localdate().year

    mounts = [
        'Январь', 'Февраль', 'Март',
        'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь',
        'Октябрь', 'Ноябрь', 'Декабрь'
    ]

    years = []
    for i in range(year-5, year+2):
        years.append(i)

    return years, mounts, year, month


def perf_main(request):
    """
    Показываем пользователю все документы за месяц года. По умолчанию - текущий.

    """
    if not request.user.is_authenticated:
        return redirect('login')

    err = None
    years, mounts, current_year, current_month = array_for_date_selection()

    if request.method == 'POST':
        req_post = request.POST
        this_add = req_post.get('add')
        select_data = req_post.get('select_data')

        # Добавление нового документа
        if this_add:
            try:
                doc_number = int(req_post.get('doc_number'))
                doc_data = req_post.get('doc_data')
                doc_data = datetime.strptime(doc_data, '%Y-%m-%d')
                description = req_post.get('description')

                if CreatedProducts.objects.filter(doc_number=doc_number):
                    err = f'Документ с номером {doc_number} уже существует'

                elif CreatedProducts.objects.filter(doc_data=doc_data):
                    err = f'Документ на дату {doc_data} уже существует'

                if not err:
                    CreatedProducts.objects.create(doc_data=doc_data, doc_number=doc_number,
                                               percent=0.0, description=description)

            except Exception as ex:
                print(ex)

        # Изменение даты выборки документов
        if select_data:
            current_year = int(req_post.get('year'))
            current_month = int(req_post.get('mount'))

    elif request.method == 'GET':
        req_get = request.GET
        doc_id = req_get.get('del_doc')
        if doc_id:
            doc_id = int(doc_id)
            doc = CreatedProducts.objects.filter(id=doc_id).first()
            if doc:
                doc.delete()

    # получаем документы выработки
    docs = CreatedProducts.objects.filter(doc_data__month=current_month, doc_data__year=current_year)

    context = {
        'created_docs': docs,
        'err': err,
        'years': years,
        'mounts': mounts,
        'current_year': current_year,
        'current_month': current_month,
    }

    return render(request, 'docs_list.html', context=context)


def perf_doc_show(request):
    """
    Просмотр и редактирование содержимого документа

    """
    if not request.user.is_authenticated:
        return redirect('login')

    # GET запрос должен быть обязательно
    reqweb = request.GET
    doc_id = reqweb.get('doc_id')
    del_wk = reqweb.get('del_wk')
    del_pr = reqweb.get('del_pr')
    err = None

    if not doc_id:
        return HttpResponse('<h3>Документ не выбран</h3>')

    doc_id = int(doc_id)
    doc = CreatedProducts.objects.filter(id=doc_id).first()
    if not doc:
        return HttpResponse('<h3>Документ не существует</h3>')

    # Удаляем из документа сотрудника
    if del_wk:
        obj = Brigade.objects.filter(id=int(del_wk)).first()
        if obj:
            obj.delete()

    # Удаляем из документа продукцию
    if del_pr:
        obj = Production.objects.filter(id=int(del_pr)).first()
        if obj:
            obj.delete()
            recalc_percent_doc(doc_id)

    if request.method == 'POST':
        # Добавление записей в документ
        req_post = request.POST
        this_add = req_post.get('add')
        if this_add:
            if this_add == 'wk_add':
                # Добавление сотрудника
                emp_id = int(req_post.get('emp_id'))

                # Проверим наличие сотрудника, если нет, то добавляем
                if Brigade.objects.filter(doc_id=doc_id, employee_id=emp_id):
                    err = 'Сотрудник уже добавлен'

                else:
                    working = req_post.get('working')
                    working = datetime.strptime(working, "%H:%M" if len(working) == 5 else "%H:%M:%S")
                    Brigade.objects.create(doc_id=doc_id, employee_id=emp_id, working=working.time())

            elif this_add == 'pr_add':
                # Добавление изделия
                product_id = int(req_post.get('product_id'))
                quantity = int(req_post.get('quantity'))
                quota = Product.objects.get(id=product_id).quota
                percent = quantity * 100 / quota
                Production.objects.create(doc_id=doc_id, product_id=product_id, quantity=quantity, percent=percent)

                recalc_percent_doc(doc_id)  #

    # связанная с документом выработка продукции
    doc_created_products = Production.objects.filter(doc_id=doc.id)
    products = Product.objects.all()

    # связанная с документом сотрудники бригада
    doc_brigade = Brigade.objects.filter(doc_id=doc.id)
    employees = Employee.objects.all()

    context = {
        'doc': doc,
        'doc_created_products': doc_created_products,
        'doc_brigade': doc_brigade,
        'products': products,
        'employees': employees,
        'err': err,
    }

    return render(request, 'doc_show.html', context=context)


def dict_view(request):
    """
    Просмотр и редактирование справочников

    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        reqweb = request.GET
        dict = reqweb.get('dict')

        if dict == 'empl':
            pass

        elif dict == 'prod':
            pass

    context = {
        'dicts': {'empl': 'Сотрудники', 'prod': 'Изделия'},
    }

    return render(request, 'dicts.html', context=context)


def report_view(request):
    """
    Выводим:
    1) проценты выработки по дням;
    2) Коэффициенты производительности работников.
    За месяц года (по умолчанию - текущий).

    """
    if not request.user.is_authenticated:
        return redirect('login')

    years, mounts, current_year, current_month = array_for_date_selection()

    if request.method == 'POST':
        req_post = request.POST
        select_data = req_post.get('select_data')
        if select_data:
            current_year = int(req_post.get('year'))
            current_month = int(req_post.get('mount'))

    # для отчета по общей производительности
    docs = CreatedProducts.objects.filter(doc_data__month=current_month, doc_data__year=current_year)
    percent_avg = docs.aggregate(Avg('percent'))['percent__avg']

    # для отчета по КП сотрудников:
    # Чтобы сотрудник получил коэффициент равный 1.0, ему нужно отработать 10560 минут в месяц
    # т.е. (22 дня * 8 час * 60 мин)
    NORMA_MIN = 10560

    # Выборка всех работавших в текущем месяце
    sample = Brigade.objects.filter(doc__doc_data__month=current_month, doc__doc_data__year=current_year)

    # вычислим суммарное время работы сотрудников за текущий месяц в минутах
    workers = {}
    for obj in sample:
        if obj.employee in workers:
            workers[obj.employee] += obj.working.hour * 60 + obj.working.minute
        else:
            workers[obj.employee] = obj.working.hour * 60 + obj.working.minute

    for key, value in workers.items():
        workers[key] = value / NORMA_MIN

    context = {
        'docs': docs,
        'years': years,
        'mounts': mounts,
        'current_year': current_year,
        'current_month': current_month,
        'percent_avg': percent_avg,
        'workers': workers,
    }

    return render(request, 'reports.html', context=context)