<h1 align="center">Приложение на Django для расчета коэффициента производительности рабочих производственного предприятия</h1>

<h2>Обзор проекта</h2>
<p>Основная цель приложения получить коэффициенты производительности (КП) работников и производительность 
  предприятия за рабочий месяц для расчета оплаты труда работников и анализа производительности предприятия руководством.</p>
<p>Для этого в приложении создаются, ответственными пользователями, документы выработки продукции в течении месяца 
  за каждый день работы предприятия. В документы выработки заносятся сделанная (обработанная) продукция и её количество. 
  Также в документ записываются рабочие, которые эту продукцию произвели, и время которые они затратили.</p>

<h2>Авторизация</h2>  
<p>Для того, что бы работать с приложением, необходимо авторизироваться.
Логин и пароль пользователям создаёт администратор даного приложения.</p>
<p align="center"><img src="/images/autoriz_form.png"></p>
<p>Для тестовой версии существующего приложения: Логин: админ Пароль: 12345</p>

<h2>Домашняя страница</h2>  
<p>После авторизации, пользователь попадает на домашнюю страницу проекта.</p>
<p>На странице выводятся все документы по выработке продукции за текущий месяц. В случае необходимости можно поменять текущий месяц.
В форме на странице можно добавить новый документ выработки. Один документ для одного рабочего дня.</p>
<p align="center"><img src="/images/main_window.png"></p>
<p>По ссылке в названии документа можно перейти на страницу редактирования документа выработки</p>

<h2>Документ выработки</h2>
<p>Центральным объектом проекта служит Документ выработки. В него заносятся даные по произведенному объему продукции и 
  временные затраты работников производства</p>
<p>Документ содержит две подчиненных таблицы и две формы для дополнения записей в эти таблицы. 
  Рядом с каждой строкой таблиц есть кнопка для удаления строки.</p>
<p align="center"><img src="/images/document.png"></p>
<p>Расчет процента выработки изделий производится по формуле:</p>
<p align="center"><i>Процент выработки за день = Количество произведенных изделий / Объем дневной нормы</i></p>
<p>Но до того как работать с документом, необходимо заполнить справочники.</p>

<h2>Справочники</h2>
<p>В приложении имеются два справочника Рабочие и Изделия:</p>
<p align="center"><img src="/images/dictions_menu.png"></p>

<h3>Рабочие</h3>
<p>В справочнике хранятся все работники, работающие сейчас или работали раньше. Страница списка содержит форму 
  для добавления нового рабочего.</p>
<p align="center"><img src="/images/dict_workers.png"></p>
<p>При переходе по ссылке ФИО, открывается форма для просмотра и редактирования элемента справочника.</p>
<p align="center"><img src="/images/edit_worker_form.png"></p>

<h3>Изделия</h3>
<p>В данном справочнике храняться все изделия, которые когда либо выпускались.</p>
<p>Элемент этого справочника содержит важную характеристику — Норма. Она выражена в количественном выражении 
для 100% выработке за день. Список изделий имеет форму для добавления нового изделия.</p>
<p align="center"><img src="/images/dict_products.png"></p>
<p>При переходе по ссылке Артикул открывается страница для просмотра и редактирования элемента справочника.</p>
<p align="center"><img src="/images/edit_product_form.png"></p>

<h2>Отчет</h2>
<p>Итогом работы приложения является отчет за текущий месяц.</p>
<p align="center"><img src="/images/reports.png"></p>
<p>Отчет содержит:</p>
<p>1. Отчет о производительности производственного предприятия согласно с нормами выработки за месяц (для администрации)</p>
<p>2. Отчет о коэффициенте производительности (КП)  рабочих, для расчета премиальной части оклада. (для бухгалтерии) </p>
<p>Формула для расчета КП</p>
<p align="center"><i>КП рабочего = Время затраченное рабочим за месяц мин/ (22дня * 8час * 60мин)</i></p>
