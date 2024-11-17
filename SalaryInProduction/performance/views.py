from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.utils.timezone import localdate
from django.db.models import Sum
from .models import CreatedProducts, Production, Brigade, Product, Employee


def perf_main(request):
    """
    Показываем пользователю все документы за месяц года. По умолчанию - текущий.
    """

    if request.method == 'POST':
        req_post = request.POST
        this_add = req_post.get('add')

        # Добавление нового документа
        if this_add:
            try:
                doc_number = int(req_post.get('doc_number'))
                doc_data = req_post.get('doc_data')
                doc_data = datetime.strptime(doc_data, '%Y-%m-%d')
                description = req_post.get('description')

                CreatedProducts.objects.create(doc_data=doc_data, doc_number=doc_number,
                                               percent=0.0, description=description)
            except Exception as ex:
                print(ex)

    elif request.method == 'GET':
        req_get = request.GET
        doc_id = req_get.get('del_doc')
        if doc_id:
            doc_id = int(doc_id)
            doc = CreatedProducts.objects.filter(id=doc_id).first()
            if doc:
                doc.delete()

    current_month = localdate().month
    current_year = localdate().year

    # получаем документы выработки
    docs = CreatedProducts.objects.filter(doc_data__month=current_month, doc_data__year=current_year)

    context = {
        'created_docs': docs,
    }

    return render(request, 'docs_list.html', context=context)


def recalc_percent_doc(doc_id):
    """
    Пересчет общего процента выработки
    :param doc_id: id документа
    """

    total_percent = Production.objects.filter(doc_id=doc_id).aggregate(Sum('percent'))['percent__sum']
    CreatedProducts.objects.filter(id=doc_id).update(percent=total_percent)


def perf_doc_show(request):
    """
    Просмотр и редактирование содержимого документа
    """

    # GET запрос должен быть обязательно
    reqweb = request.GET
    doc_id = reqweb.get('doc_id')
    del_wk = reqweb.get('del_wk')
    del_pr = reqweb.get('del_pr')

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

                recalc_percent_doc(doc_id)

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
    }

    return render(request, 'doc_show.html', context=context)


def dict_view(request):

    context = {
        'dicts': {'empl': 'Сотрудники', 'prod': 'Изделия'},
    }

    return render(request, 'dicts.html', context=context)
