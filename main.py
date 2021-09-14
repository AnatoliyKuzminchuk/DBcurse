from flask import Flask, render_template, url_for, request, abort, flash
import mysql.connector
from decimal import Decimal
import datetime


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL2021",
    database="autoparts_store"
)
cursor = mydb.cursor()
table_names = ['catalog', 'clients', 'applications_pending', 'defects', 'overheads', 'supplier_orders', 'suppliers',
               'warehouse', 'warehouse_orders', 'warehouse_sections', 'cash']
suppliers_id = list()
catalog_id = list()
clients_id = list()
defects_id = list()
warehouse_id = list()
warehouse_sections_id = list()
warehouse_orders_id = list()
supplier_orders_id = list()
supplier_orders_id_not_ex = list()
overheads_id = list()


def catalog_list_filling():
    global catalog_id
    catalog_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM catalog""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        catalog_id += [i]


def suppliers_list_filling():
    global suppliers_id
    suppliers_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM suppliers""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        suppliers_id += [i]


def clients_list_filling():
    global clients_id
    clients_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM clients""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        clients_id += [i]


def defects_list_filling():
    global defects_id
    defects_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM defects""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        defects_id += [i]


def warehouse_list_filling():
    global warehouse_id
    warehouse_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM warehouse""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        warehouse_id += [i]


def warehouse_sections_list_filling():
    global warehouse_sections_id
    warehouse_sections_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM warehouse_sections""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        warehouse_sections_id += [i]


def warehouse_orders_list_filling():
    global warehouse_orders_id
    warehouse_orders_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM warehouse_orders""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        warehouse_orders_id += [i]


def supplier_orders_list_filling():
    global supplier_orders_id
    supplier_orders_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM supplier_orders""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        supplier_orders_id += [i]


def overheads_list_filling():
    global overheads_id
    overheads_id = list()
    cursor.execute("""SELECT MAX(`id`) FROM overheads""")
    id = cursor.fetchall()
    for i in range(1, id[0][0] + 1):
        overheads_id += [i]


def supplier_orders_id_not_ex_filling():
    global supplier_orders_id_not_ex
    supplier_orders_id_not_ex = list()
    cursor.execute("""SELECT id FROM supplier_orders where executed = 0""")
    id = cursor.fetchall()
    for i in id:
        supplier_orders_id_not_ex += [int(i[0])]


def lists_filling():
    catalog_list_filling()
    suppliers_list_filling()
    clients_list_filling()
    defects_list_filling()
    warehouse_list_filling()
    warehouse_sections_list_filling()
    warehouse_orders_list_filling()
    supplier_orders_list_filling()
    overheads_list_filling()


def NotNull(condition):
    if condition == '':
        return True
    else:
        return False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdasfhadofuhy8w278yhdoisufy979dys9fya9sd7yf9'

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_error(e):
    mydb.rollback()
    return render_template("500.html")


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/suppliers')
def suppliers():
    return render_template("suppliers.html")


@app.route('/details')
def details():
    return render_template("details.html")


@app.route('/clients')
def clients():
    return render_template("clients.html")


@app.route('/warehouse')
def warehouse():
    return render_template("warehouse.html")


@app.route('/overheads')
def overheads():
    return render_template("overheads.html")


@app.route('/defects')
def defects():
    return render_template("defects.html")


@app.route('/work')
def work():
    return render_template("work.html")


@app.route('/<string:table_name>/select')
def select_table(table_name):
    if table_name not in table_names:
        abort(404)
    with mydb.cursor() as cursor:
        cursor.execute('SELECT * FROM {} ORDER BY 1'.format(table_name))
        columns = [desc[0] for desc in cursor.description]
        records = cursor.fetchall()
    defenit = 'All'
    return render_template("table.html", table=records, columns=columns, title=table_name, id_first=True,
                           length=len(records), defenition=defenit)


@app.route('/details/<int:num>', methods=['GET', 'POST'])
def details_fun(num):
    """Get data about a specific kind of parts part_id: which suppliers
    shipped, what are their rates and delivery time."""
    if num == 1:
        if request.method == 'GET':
            return render_template("form4.html", values=catalog_id)
        elif request.method == "POST":
            condition1 = request.form['id']
            cursor.execute(
                """with supplier_id as (select distinct supplier from Supplier_Orders where 
                   part=%s) select id, name, percentage_price*(select price from Catalog 
                   where id=%s)/100 as price, time_of_delivery from Suppliers, supplier_id 
                   where supplier_id.supplier=Suppliers.id order by id""", [condition1, condition1])

            defenit = 'List of providers who provide details type: ' + condition1
    """Display the ten best-selling parts in ascending order."""
    if num == 2:
        if request.method == 'GET':
            cursor.execute(
                """with sold_parts as (select part, sum(number) as total_number from Warehouse_Orders group 
                   by part order by total_number desc limit 10) select part, total_number
                   from sold_parts order by total_number""")

            defenit = 'Top 10 details(req_5_1)'
    """Get the average number of sales per month for each type of part."""
    if num == 3:
        if request.method == 'GET':
            cursor.execute(
                """with months as (select TIMESTAMPDIFF(month, min(date), max(date)) as total_months 
                            from Warehouse_Orders), parts_sales as (select part, sum(number) as total_number 
                            from Warehouse_Orders group by part) select part, total_number/(select months.total_months 
                            from months) as sales_per_month from parts_sales;""")
            defenit = 'Sales per mounth'
    """Add new detail to catalog"""
    if num == 4:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('catalog'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form16.html", table=records,
                                   columns=columns, title='Catalog', id_first=True)
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = int(request.form['param2'])
            condition3 = int(request.form['param3'])
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('catalog'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            if NotNull(condition1):
                flash("Please enter detail name", category='error')
                return render_template("form16.html", table=records,
                                   columns=columns, title='Catalog', id_first=True)
            if condition2 <= 0:
                flash("Please enter detail cost", category='error')
                return render_template("form16.html", table=records,
                                   columns=columns, title='Catalog', id_first=True)
            if condition3 <= 0:
                flash("Please enter detail size", category='error')
                return render_template("form16.html", table=records,
                                   columns=columns, title='Catalog', id_first=True)
            from tables_filling import insert_catalog
            insert_catalog(engine, condition1, condition2, condition3)
            flash("Detail add success", category='success')
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('catalog'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            catalog_list_filling()
            return render_template("form16.html", table=records,
                                   columns=columns, title='Catalog', id_first=True)
    """Catalog update"""
    if num == 5:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('catalog'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form17.html", values=catalog_id, table=records,
                                   columns=columns, title='Catalog', id_first=True, )
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = int(request.form['param2'])
            condition3 = int(request.form['param3'])
            condition4 = int(request.form['param4'])
            if NotNull(condition1):
                temp = engine.execute(f"""select name from catalog where id='{condition4}'""").fetchall()
                condition1 = temp[0][0]
            if condition2 <= 0:
                cost = engine.execute(f"""select price from catalog where id='{condition4}'""").fetchall()
                condition2 = cost[0][0]
            if condition3 <= 0:
                temp = engine.execute(f"""select size from catalog where id='{condition4}'""").fetchall()
                condition3 = temp[0][0]
            engine.execute(f"""update catalog set name = '{condition1}', price = '{condition2}'
                            , size = '{condition3}' where id='{condition4}'""")
            flash("Catalog succesfully changed", category='error')
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('catalog'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            catalog_list_filling()
            return render_template("form17.html", table=records,
                                   columns=columns, title='Catalog', id_first=True, )
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return render_template("table.html", table=records, columns=columns, title='Details', id_first=True,
                           length=len(records), defenition=defenit)


@app.route('/suppliers/<int:num>', methods=['GET', 'POST'])
def suppliers_fun(num):
    """Get a list of category suppliers supplying part_id."""
    if num == 1:
        if request.method == 'GET':
            return render_template("form1.html", values=catalog_id)
        elif request.method == "POST":
            condition1 = request.form['param1']
            id_by = request.form['id_by']

        if condition1 == 'All':
            cursor.execute(
                """with sellers as(select distinct supplier from 
                Supplier_Orders where part='{}') select id, name from Suppliers, 
                sellers where sellers.supplier=Suppliers.id""".format(id_by))
            defenit = 'Suppliers which sold details with number: ' + id_by

        else:
            cursor.execute(
                """with sellers as(select distinct supplier from Supplier_Orders 
                where part='{}') select id, name from Suppliers, sellers 
                where sellers.supplier=Suppliers.id and Suppliers.type='{}'""".format(id_by, condition1))
            defenit = 'Suppliers ' + condition1 + ' which sold details with number: ' + id_by
    """Retrieve a list of category suppliers that have awarded at least
    threshold_number of parts part_id for the time from date_1 to date_2 """
    if num == 2:
        if request.method == 'GET':
            return render_template("form2.html", values=catalog_id)
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = request.form['param2']
            condition3 = request.form['param3']
            condition4 = request.form['param4']
            id_by = request.form['id_by']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""with sellers as (with suppliers_and_numbers as (select supplier, sum(number) as 
                            total_number from Supplier_Orders where part=%s and date between %s and 
                            %s  group by supplier) select supplier from suppliers_and_numbers where 
                            total_number>= %s) select id, name from Suppliers, sellers where
                            sellers.supplier=Suppliers.id and Suppliers.type=%s
                                            """, [id_by, condition2, condition3, condition1, condition4])
            defenit = 'Suppliers'
    """Display the ten "cheapest"suppliers in ascending order."""
    if num == 3:
        if request.method == 'GET':
            cursor.execute(
                """select id, name, percentage_price as percent from Suppliers order by percentage_price limit 10""")
            defenit = 'Top 10 suppliers(req_5_2)'
    """Get the share of goods of a specific supplier id in units of goods for the time from param2 to param3."""
    if num == 4:
        if request.method == 'GET':
            return render_template("form6.html", values=suppliers_id)
        elif request.method == "POST":
            condition1 = request.form['id']
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select supplier as id, sum(number)/(select sum(number) from Warehouse_Orders where supplier!=%s) 
                              as Total_number_part, number as Amount, suppliers.name as Suppliers_name from 
                              Warehouse_Orders join suppliers on suppliers.id=Warehouse_Orders.supplier where 
                              supplier=%s and date between %s and %s""",
                           [condition1, condition1, condition2, condition3])
            defenit = 'Supplier part on numbers/turnover #: ' + condition1 + ' between ' + condition2 + ' and ' + condition3
    """Get the share of goods of a specific supplier id as a percentage of goods for the time from param2 to param3."""
    if num == 5:
        if request.method == 'GET':
            return render_template("form6.html", values=suppliers_id)
        elif request.method == "POST":
            condition1 = request.form['id']
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select supplier as id, sum(number)/(select sum(number) from Warehouse_Orders)*100 
                              as Total_percent_part, number as Amount, suppliers.name as Suppliers_name from 
                              Warehouse_Orders join suppliers on suppliers.id=Warehouse_Orders.supplier where 
                              supplier=%s and date between %s and %s""", [condition1, condition2, condition3])
            defenit = 'Supplier part on percent/turnover #: ' + condition1 + ' between ' + condition2 + ' and ' + condition3
    """Get the share of goods of a particular supplier id in cents of goods for the time from param2 to param3."""
    if num == 6:
        if request.method == 'GET':
            return render_template("form6.html", values=suppliers_id)
        elif request.method == "POST":
            condition1 = request.form['id']
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select supplier as id, sum(number)*(select catalog.price where catalog.id=Warehouse_Orders.part) 
            as Total_money_part, catalog.price as Price, number as Amount, suppliers.name as Suppliers_name from Warehouse_Orders 
            join suppliers on suppliers.id=Warehouse_Orders.supplier join catalog on catalog.id=Warehouse_Orders.part where supplier=%s 
	        and catalog.id=Warehouse_Orders.part and date between %s and %s""", [condition1, condition2, condition3])
            defenit = 'Supplier part on money/turnover #: ' + condition1 + ' between ' + condition2 + ' and ' + condition3
    """Get the share of the goods of a particular supplier id in cents of the goods for the time from param2 to param3.
         admittedly outbound arrival """
    if num == 7:
        if request.method == 'GET':
            return render_template("form6.html", values=suppliers_id)
        elif request.method == "POST":
            condition1 = request.form['id']
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select supplier as id, sum(number)*(select catalog.price where catalog.id=Warehouse_Orders.part) as Total_money_part, 
                              (select sum(number)*(select catalog.price where catalog.id=Warehouse_Orders.part) as Total_money from Warehouse_Orders 
                              join catalog on catalog.id=Warehouse_Orders.part where catalog.id=Warehouse_Orders.part and date between %s and %s) as Total_input, catalog.price as Price, 
                              number as Amount, suppliers.name as Suppliers_name from Warehouse_Orders 
                              join suppliers on suppliers.id=Warehouse_Orders.supplier join catalog on catalog.id=Warehouse_Orders.part 
                              where supplier=%s and catalog.id=Warehouse_Orders.part and date between %s and %s""",
                           [condition2, condition3, condition1, condition2, condition3])
            defenit = 'Supplier part on money/input #: ' + condition1 + ' between ' + condition2 + ' and ' + condition3
    """Add new supplier"""
    if num == 8:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('suppliers'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form20.html", table=records,
                                   columns=columns, title='Suppliers', id_first=True)
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = request.form['param2']
            condition3 = request.form['param3']
            condition4 = int(request.form['param4'])
            condition5 = int(request.form['param5'])
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Suppliers'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            from tables_filling import insert_suppliers
            if NotNull(condition1):
                flash("Please enter name", category='error')
                return render_template("form20.html", table=records,
                                       columns=columns, title='Suppliers', id_first=True)
            if NotNull(condition2):
                flash("Please enter country", category='error')
                return render_template("form20.html", table=records,
                                       columns=columns, title='Suppliers', id_first=True)
            if condition4 <= 0:
                flash("Please enter time", category='error')
                return render_template("form20.html", table=records,
                                       columns=columns, title='Suppliers', id_first=True)
            if condition5 <= 0:
                flash("Please enter percetage", category='error')
                return render_template("form20.html", table=records,
                                       columns=columns, title='Suppliers', id_first=True)
            insert_suppliers(engine, condition1, condition2, condition3, condition4, condition5)
            flash("Supplier add success", category='success')
            overheads_list_filling()
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('suppliers'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            suppliers_list_filling()
            return render_template("form20.html", table=records,
                                   columns=columns, title='Suppliers', id_first=True)
    """Suppliers update"""
    if num == 9:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Suppliers'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form21.html", values=suppliers_id, table=records,
                                   columns=columns, title='Suppliers', id_first=True, )
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = request.form['param2']
            condition3 = request.form['param3']
            condition4 = int(request.form['param4'])
            condition5 = int(request.form['param5'])
            condition6 = int(request.form['param6'])
            if NotNull(condition1):
                temp = engine.execute(f"""select name from Suppliers where id='{condition6}'""").fetchall()
                condition1 = temp[0][0]
            if NotNull(condition2):
                temp = engine.execute(f"""select country from Suppliers where id='{condition6}'""").fetchall()
                condition2 = temp[0][0]
            if NotNull(condition3):
                temp = engine.execute(f"""select type from Suppliers where id='{condition6}'""").fetchall()
                condition3 = temp[0][0]
            if condition4 <= 0:
                temp = engine.execute(f"""select time_of_delivery from Suppliers where id='{condition6}'""").fetchall()
                condition4 = temp[0][0]
            if condition5 <= 0:
                temp = engine.execute(f"""select percentage_price from Suppliers where id='{condition6}'""").fetchall()
                condition5 = temp[0][0]
            engine.execute(f"""update Suppliers set name = '{condition1}', country = '{condition2}',
            type = '{condition3}', time_of_delivery = '{condition4}', percentage_price = '{condition5}' where id='{condition6}'""")
            flash("Supplier succesfully changed", category='error')
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Suppliers'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            catalog_list_filling()
            return render_template("form21.html", table=records,
                                   columns=columns, title='Suppliers', id_first=True, )
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return render_template("table.html", table=records, columns=columns, title='Suppliers', id_first=True,
                           length=len(records), defenition=defenit)


@app.route('/clients/<int:num>', methods=['GET', 'POST'])
def clients_fun(num):
    """Get a list of buyers who bought the item id during the period from param2 to param3."""
    if num == 1:
        if request.method == 'GET':
            return render_template("form4.html", values=catalog_id)
        elif request.method == "POST":
            condition2 = request.form['param2']
            condition3 = request.form['param3']
            condition1 = request.form['id']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select id, name, phone from clients where 
                            `clients`.`id` = (select distinct client from warehouse_orders 
                            where date between %s and %s and part=%s) order by id""",
                           [condition2, condition3, condition1])
            defenit = 'Clients who buy detail type: ' + condition1 + ', between ' + condition2 + ' : ' + condition3
    """Get a list of buyers who bought a id product in an amount no less than threshold_number."""
    if num == 2:
        if request.method == 'GET':
            return render_template("form5.html", values=clients_id)
        elif request.method == "POST":
            id = request.form['id']
            cursor.execute(
                """select id, name, phone from clients where `clients`.`id` = 
                (with client_total as (select client, number from warehouse_orders where part=%s
                group by client) select client from client_total where number>=%s) """, [id, id])
            defenit = 'Clients who buy detail type: ' + id
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return render_template("table.html", table=records, columns=columns, title='Details', id_first=True,
                           length=len(records), defenition=defenit)


@app.route('/warehouse/<int:num>', methods=['GET', 'POST'])
def warehouse_fun(num):
    """Get inventory, volume and bin number for all parts in stock."""
    if num == 1:
        if request.method == 'GET':
            cursor.execute(
                """with sections as(select distinct section from warehouse) select part_type, id as 
                    section_number, total_size from Warehouse_Sections, sections 
                    where Warehouse_Sections.id=sections.section order by part_type""")
            defenit = 'List from warehouse for request number 4'
    """Get a list of unsold goods in the warehouse for a certain period"""
    if num == 2:
        if request.method == 'GET':
            return render_template("form7.html")
        elif request.method == "POST":
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""with sections_wn as (select section, sum(number) as warehouse_number from warehouse
                            where date between %s and %s group by section) select part_type as Detail_type, 
                            sum(warehouse_number) as Warehouse_rest from sections_wn, Warehouse_Sections 
                            where sections_wn.section=Warehouse_Sections.id group by part_type""",
                           [condition2, condition3])
            defenit = 'Warehouse rest list between ' + condition2 + ' and ' + condition3
    """Get the volume of unsold goods in the warehouse for a certain 
    period from param2 to param3 of the total goods as a percentage."""
    if num == 3:
        if request.method == 'GET':
            return render_template("form7.html")
        elif request.method == "POST":
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'
            cursor.execute("""with number_with_date as ( with temp_table as (select number, supplier, date 
                           from Supplier_Orders where executed=true) select number, 
                           date_add(date, interval time_of_delivery day) as date_of_arrival
                           from temp_table, Suppliers where temp_table.supplier=Suppliers.id)
                           select sum(number) as total_p from number_with_date where date_of_arrival 
                           between %s and %s""", [condition2, condition3])
            total_come = cursor.fetchall()
            cursor.execute("""with number_with_date as ( with temp_table as (select number, supplier, date 
                           from warehouse) select number, 
                           date_add(date, interval time_of_delivery day) as date_of_arrival
                           from temp_table, Suppliers where temp_table.supplier=Suppliers.id)
                           select sum(number) as total_unsold from number_with_date where date_of_arrival 
                           between %s and %s""", [condition2, condition3])
            total_sold = cursor.fetchall()
            if len(total_sold) == 0:
                return None
            else:
                total_sold = total_sold[0][0]
                if total_sold == 0:
                    return None
            if len(total_come) == 0:
                return 0
            else:
                total_come = total_come[0][0]
            records = (total_sold / total_come * 100).quantize(Decimal("1.00"))
            total_sold = total_sold.quantize(Decimal("1.00"))
            total_come = total_come.quantize(Decimal("1.00"))
            defenit = 'Warehouse rest'
            return render_template("output.html", table=records, title='Warehouse', id_first=True,
                                   length=1, defenition=defenit, output3=records, text3='Percent of sold details: ',
                                   output1=total_sold, text1='Quantity of sold details: ', output2=total_come,
                                   text2='Quantity of income details: ')
    """Calculate how many empty cells there are in the warehouse and how many it can hold."""
    if num == 4:
        if request.method == 'GET':
            cursor.execute("""with temp_table as (select section, sum(number) as section_number from warehouse 
                            group by section) select count(*) as empty_sections from warehouse_sections where id not in 
                            (select section from temp_table where section_number > 0);""")
            empty_sect = cursor.fetchall()
            empty_sect = empty_sect[0][0]
            cursor.execute("""with fulfill as (with temp_table as (with temp_table as (select section, sum(number) as 
                            section_number from warehouse group by section) select part_type, sum(section_number) 
                            as part_number from warehouse_sections, temp_table where 
                            warehouse_sections.id=temp_table.section) select sum(part_number*size) as not_free_size from
                            temp_table, catalog where temp_table.part_type=catalog.id),
                            total_size as (select sum(total_size) as all_size from warehouse_sections)
                            select (all_size-not_free_size) as free_size from fulfill, total_size""")
            free_size = cursor.fetchall()
            free_size = free_size[0][0]
            cursor.execute("""select sum(total_size) as total_capacity from warehouse_sections""")
            total_size = cursor.fetchall()
            total_size = total_size[0][0]
            defenit = 'Information about warehouse space: '
            return render_template("output.html", title='Warehouse', id_first=True, length=1, defenition=defenit,
                                   text1='Empty section: ', output1=empty_sect, text2='Free space: ', output2=free_size,
                                   text3='All space: ', output3=total_size, )
    """Add detail to warehouse"""
    if num == 5:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Warehouse'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form13.html", values=catalog_id, values1=suppliers_id, table=records,
                                   columns=columns, title='Warehouse', id_first=True)
        elif request.method == "POST":
            condition1 = int(request.form['param1'])
            condition2 = request.form['param2']
            condition3 = int(request.form['param3'])
            condition4 = int(request.form['param4'])
            if NotNull(condition2):
                today = datetime.date.today()
                condition2 = today.strftime("%Y-%m-%d")
            from tables_filling import insert_warehouse
            r_space = engine.execute(f"""with t_t as (with temp_table as (select section, sum(number) as section_number 
                                                 from warehouse group by section) select section, section_number, total_size 
                                                 from temp_table, warehouse_sections where temp_table.section=warehouse_sections.id 
                                                 and part_type='{condition1}') select section, floor(total_size / (select size from 
                                                 catalog where id='{condition1}')-section_number) as remaining_space 
                                                 from t_t""").fetchall()
            for _ in range(len(r_space)):
                condition3 -= r_space[_][1]
                if condition3 <= 0:
                    insert_warehouse(engine, r_space[_][0], condition3 + r_space[_][1], condition4, condition2)
                    break
                else:
                    insert_warehouse(engine, r_space[_][0], r_space[_][1], condition4, condition2)
            if condition3 > 0:
                flash("Warehouse is over", category='error')
            else:
                flash("Details comes to warehouse", category='success')
                mydb.commit()
                warehouse_list_filling()
                cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Warehouse'))
                columns = [desc[0] for desc in cursor.description]
                records = cursor.fetchall()
                return render_template("form13.html", values=catalog_id, values1=suppliers_id, table=records,
                                       columns=columns, title='Warehouse', id_first=True)
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return render_template("table.html", table=records, columns=columns, title='Warehouse', id_first=True,
                           length=len(records), defenition=defenit)


@app.route('/overheads/<int:num>', methods=['GET', 'POST'])
def overheads_fun(num):
    """Get overhead as a percentage of sales"""
    if num == 1:
        if request.method == 'GET':
            cursor.execute("""select sum(money) from overheads""")
            overheads = cursor.fetchall()
            cursor.execute("""select (select sum(number)*(select catalog.price where catalog.id=Warehouse_Orders.part) 
                                        as Total_money from Warehouse_Orders join catalog on catalog.id=Warehouse_Orders.part where catalog.id=Warehouse_Orders.part) 
                                        as Total_input from Warehouse_Orders join catalog on catalog.id=Warehouse_Orders.part""")
            income = cursor.fetchall()
            if len(income) == 0:
                return None
            else:
                income = income[0][0]
                if income == 0:
                    return None
            if len(overheads) == 0:
                return 0
            else:
                overheads = overheads[0][0]
            records = (overheads / income * 100).quantize(Decimal("1.00"))
            defenit = 'Overhead percent'
            return render_template("output.html", table=records, title='Overheads', id_first=True,
                                   length=1, defenition=defenit, output1=records, text1=defenit)
    """Add new Overhead"""
    if num == 2:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('overheads'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form18.html", table=records,
                                   columns=columns, title='Overheads', id_first=True)
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = request.form['param2']
            condition3 = request.form['param3']
            condition4 = int(request.form['param4'])
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('overheads'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            if NotNull(condition3):
                today = datetime.date.today()
                condition3 = today.strftime('%Y-%m-%d')
            from tables_filling import insert_overheads
            if NotNull(condition1):
                flash("Please enter overhead type", category='error')
                return render_template("form18.html", table=records,
                                   columns=columns, title='Overheads', id_first=True)
            if condition4 <= 0:
                flash("Please enter money", category='error')
                return render_template("form18.html", table=records,
                                   columns=columns, title='Overheads', id_first=True)
            insert_overheads(engine, condition1, condition2, condition3, condition4)
            flash("Overhead add success", category='success')
            overheads_list_filling()
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('overheads'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            overheads_list_filling()
            return render_template("form18.html", table=records,
                                   columns=columns, title='Overheads', id_first=True)
    """Overhead update"""
    if num == 3:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Overheads'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form19.html", values=overheads_id, table=records,
                                   columns=columns, title='Overheads', id_first=True )
        elif request.method == "POST":
            condition1 = request.form['param1']
            condition2 = request.form['param2']
            condition3 = request.form['param3']
            condition4 = int(request.form['param4'])
            condition5 = int(request.form['param5'])
            if NotNull(condition1):
                temp = engine.execute(f"""select type from overheads where id='{condition4}'""").fetchall()
                condition1 = temp[0][0]
            if NotNull(condition2):
                temp = engine.execute(f"""select explanation from overheads where id='{condition4}'""").fetchall()
                condition2 = temp[0][0]
            if NotNull(condition3):
                temp = engine.execute(f"""select date from overheads where id='{condition4}'""").fetchall()
                condition3 = temp[0][0]
            if condition5 <= 0:
                temp = engine.execute(f"""select money from overheads where id='{condition4}'""").fetchall()
                condition3 = temp[0][0]
            engine.execute(f"""update overheads set type = '{condition1}', explanation = '{condition2}'
                                , date = '{condition3}', money = '{condition5}' where id='{condition4}'""")
            engine.execute(f"""update cash set cash = '{-condition5}' where overhead_id='{condition4}'""")
            flash("Overhead succesfully changed", category='error')
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('Overheads'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            catalog_list_filling()
            return render_template("form19.html", table=records,
                                   columns=columns, title='Overheads', id_first=True, )


@app.route('/defects/<int:num>', methods=['GET', 'POST'])
def defects_fun(num):
    """Get a list of defective goods that came in a certain period."""
    if num == 1:
        if request.method == 'GET':
            return render_template("form8.html")
        elif request.method == "POST":
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select part as Detail_Type, sum(number) as Quantity_Of_Details from Defects 
                            where date between %s and %s group by part""",
                           [condition2, condition3])
            defenit = 'Defects list by date ' + condition2 + ' and ' + condition3
    """Get a list of suppliers of defective goods that have arrived in a certain period."""
    if num == 2:
        if request.method == 'GET':
            return render_template("form8.html")
        elif request.method == "POST":
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""select distinct(supplier) as Defects_supplier, number as Quantity, name as Company_name from Defects 
                            join suppliers on suppliers.id = `defects`.`supplier`
                            where date between %s and %s""",
                           [condition2, condition3])
            defenit = 'Defects suppliers list by date ' + condition2 + ' and ' + condition3
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return render_template("table.html", table=records, columns=columns, title='Defects', id_first=True,
                           length=len(records), defenition=defenit)


@app.route('/work/<int:num>', methods=['GET', 'POST'])
def work_fun(num):
    """Get a list of goods sold for a day."""
    if num == 1:
        if request.method == 'GET':
            return render_template("form9.html")
        elif request.method == "POST":
            condition2 = request.form['param2']

            if NotNull(condition2):
                condition2 = '2020-01-13'

            cursor.execute("""select part as id, sum(number) as Detail_quantity from warehouse_orders 
                            where date=%s and number>0 group by part""",
                           [condition2])
            defenit = 'Sold details at date ' + condition2
    """Get the value of goods sold for a day."""
    if num == 2:
        if request.method == 'GET':
            return render_template("form8.html")
        elif request.method == "POST":
            condition2 = request.form['param2']

            if NotNull(condition2):
                condition2 = '2020-01-13'

            cursor.execute("""select sum(number) as Total_quantity from warehouse_orders 
                            where date=%s and number>0""",
                           [condition2])
            total_quantity = cursor.fetchall()
            cursor.execute("""with temp_table as (select part, sum(number) as number_of_parts from warehouse_orders 
                            where date=%s group by part) select sum(number_of_parts*price) as total_price 
                            from temp_table, catalog where catalog.id=temp_table.part;""",
                           [condition2])
            total_sum = cursor.fetchall()
            if len(total_quantity) == 0:
                return None
            else:
                total_quantity = total_quantity[0][0]
                if total_quantity == 0:
                    return None
            if len(total_sum) == 0:
                return 0
            else:
                total_sum = total_sum[0][0]
            defenit = 'Sold data by day' + condition2
            return render_template("output.html", title='Work', id_first=True,
                                   length=1, defenition=defenit, output1=total_quantity,
                                   text1="Quantity of sold details: ", output2=total_sum,
                                   text2="Money from of sold details: ")
    """Receive a cash report for a period."""
    if num == 3:
        if request.method == 'GET':
            return render_template("form10.html")
        elif request.method == "POST":
            condition2 = request.form['param2']
            condition3 = request.form['param3']

            if NotNull(condition2):
                condition2 = '2018-03-03'
            if NotNull(condition3):
                condition3 = '2021-04-03'

            cursor.execute("""with date_and_income as (with temp_table as (select date, part, number from 
                            warehouse_orders where date between %s and %s) select date, 
                            (price*number) as order_price, number from temp_table, catalog 
                            where temp_table.part=catalog.id) select date, sum(order_price) as day_income 
                            from date_and_income group by date""",
                           [condition2, condition3])
            defenit = 'Cash report between date ' + condition2 + ' and ' + condition3
    """Get an inventory sheet."""
    if num == 4:
        if request.method == 'GET':
            cursor.execute("""with t_table as (with temp_table as (select section, number from warehouse)
                            select part_type, sum(number) as total_number from  temp_table, warehouse_sections 
                            where temp_table.section=warehouse_sections.id group by part_type) select part_type as
                            id, name as Detail_name, total_number as Quantity, price as Price from t_table, 
                            catalog where t_table.part_type=catalog.id"""
                           )
            defenit = 'Inventory sheet '
    """Get the rate of turnover of funds invested in the product (how the product is quickly sold)"""
    if num == 5:
        if request.method == 'GET':
            cursor.execute("""with date_gain as (with date_and_gain as (with temp_table as (select date, part, number 
                            from warehouse_orders) select date, (price*number) as 
                            order_price from temp_table, catalog where temp_table.part=catalog.id)
                            select date, sum(order_price) as day_gain from date_and_gain group by date)
                            select sum(day_gain)/(DATEDIFF('2018-03-03','2021-03-03')) as daily_turnover_speed from date_gain"""
                           )
            defenit = 'Profit '
    """Get the total number of customer orders for the expected item."""
    if num == 6:
        if request.method == 'GET':
            cursor.execute("""select supplier_orders.id, part as Detail_type, catalog.name as Detail_name, number as Quantity,
                            clients.name as Client_name from supplier_orders join catalog on catalog.id=supplier_orders.part
                            join clients on clients.id=supplier_orders.client where executed=false and client <> 1 order by id;"""
                           )
            defenit = 'Waiting orders from clients '
    """Calculate the total amount of orders from buyers for the expected product."""
    if num == 7:
        if request.method == 'GET':
            cursor.execute("""with temp_table as (select part, sum(number) as part_number from supplier_orders where 
                            executed=false and client <> 1 group by part) select sum(part_number*price) as orders_sum 
                            from temp_table, catalog where temp_table.part=catalog.id""")
            orders_sum = cursor.fetchall()
            if len(orders_sum) == 0:
                return 0
            else:
                orders_sum = orders_sum[0][0]
            records = (orders_sum).quantize(Decimal("1.00"))
            defenit = 'Not delivered order price: '
            return render_template("output.html", table=records, title='Work', id_first=True,
                                   length=1, defenition=defenit, output1=records, text1=defenit)
    """Order detail from warehouse"""
    if num == 8:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            return render_template("form11.html", values=catalog_id, values1=clients_id)
        elif request.method == "POST":
            condition1 = int(request.form['param1'])
            condition2 = request.form['param2']
            condition3 = int(request.form['param3'])
            condition4 = int(request.form['param4'])
            if condition3 == 0:
                flash("Please enter number of details", category='error')
                return render_template("form11.html", values=catalog_id, values1=clients_id)
            if NotNull(condition2):
                today = datetime.date.today()
                condition2 = today.strftime("%Y-%m-%d")
            from tables_filling import insert_warehouse_orders, insert_supplier_orders
            cursor.execute(f"""select sum(number) as tpn from warehouse where section in (select id 
                                                    from warehouse_sections where part_type=%s)""", [condition1])
            total_in_warehouse = cursor.fetchone()
            if len(total_in_warehouse) == 0:
                total_in_warehouse = 0
            else:
                total_in_warehouse = total_in_warehouse[0]
            if total_in_warehouse is None:
                total_in_warehouse = 0
            if total_in_warehouse < condition3:
                flash("Sorry, we don't have enough details now new order to supplier created", category='success')
                cursor.execute(f"""select supplier from warehouse where section = (select id from warehouse_sections 
                                    where part_type='%s' limit 1) limit 1;""", [condition1])
                k=0
                supplier = cursor.fetchall()
                for i in range(len(supplier)):
                    supplier = supplier[0][0]
                    k=1
                if k != 1:
                    supplier=1
                insert_supplier_orders(engine, condition2, condition4, condition1, '0', condition3, supplier)
                supplier_orders_list_filling()
                mydb.commit()
                return render_template("form11.html")
            else:
                cursor.execute(f"""select section, number, supplier, id from warehouse where 
                                             section in (select id from warehouse_sections where part_type=%s) 
                                             order by section""", [condition1])
                w_parts = cursor.fetchall()
                for _ in range(len(w_parts)):
                    condition3 -= w_parts[_][1]
                    if condition3 <= 0:
                        if condition3 < 0:
                            insert_warehouse_orders(engine, condition2, condition4, condition1, w_parts[_][0], condition3 + w_parts[_][1],
                                                w_parts[_][2])
                            engine.execute(f"update warehouse set number=number-{condition3 + w_parts[_][1]} where id={w_parts[_][3]}")
                        if condition3 == 0:
                            insert_warehouse_orders(engine, condition2, condition4, condition1, w_parts[_][0],
                                                    condition3 + w_parts[_][1],
                                                    w_parts[_][2])
                            engine.execute(f"delete from warehouse where id=%s", [w_parts[_][3]])
                        break
                    else:
                        insert_warehouse_orders(engine, condition2, condition4, condition1, w_parts[_][0], w_parts[_][1],
                                                w_parts[_][2])
                        engine.execute(f"delete from warehouse where id=%s",[w_parts[_][3]])
                flash("Details sold success", category='success')
                mydb.commit()
                warehouse_orders_list_filling()
                return render_template("form11.html")
    """Shop orders modification"""
    if num == 9:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('warehouse_orders'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form14.html", values=warehouse_orders_id, values1=clients_id, table=records,
                                    columns=columns, title='Warehouse Orders', id_first=True,)
        elif request.method == "POST":
            condition1 = int(request.form['param1'])
            condition2 = request.form['param2']
            condition3 = int(request.form['param3'])
            condition4 = int(request.form['param4'])
            if condition3 == 0:
                cost = engine.execute(f"""select cost from warehouse_orders where id='{condition1}'""").fetchall()
                condition3 = cost[0][0]
            if NotNull(condition2):
                date = engine.execute(f"""select date from warehouse_orders where id='{condition1}'""").fetchall()
                condition2 = date[0][0]
            engine.execute(f"""update warehouse_orders set date = '{condition2}', client = '{condition4}', 
                                    cost = '{condition3}' where id='{condition1}'""")
            engine.execute(f"""update cash set cash = '{condition3}' where order_war_id='{condition1}'""")
            flash("Order succesfully changed", category='error')
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('warehouse_orders'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form14.html", table=records,
                                    columns=columns, title='Warehouse Orders', id_first=True,)
    """Suppliers orders modification"""
    if num == 10:
        from sqlalchemy import create_engine
        engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')
        if request.method == 'GET':
            cursor.execute('SELECT * FROM {} where executed = 0 ORDER BY 1'.format('supplier_orders'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            supplier_orders_id_not_ex_filling()
            return render_template("form15.html", values=supplier_orders_id_not_ex, values1=clients_id, table=records,
                                    columns=columns, title='Supplier Orders', id_first=True,)
        elif request.method == "POST":
            condition1 = int(request.form['param1'])
            condition2 = request.form['param2']
            condition3 = int(request.form['param3'])
            condition4 = int(request.form['param4'])
            condition5 = int(request.form['param5'])
            condition6 = int(request.form['param6'])
            if condition3 == 0:
                cost = engine.execute(f"""select cost from supplier_orders where id='{condition1}'""").fetchall()
                condition3 = cost[0][0]
            if condition6 == 0:
                number = engine.execute(f"""select number from supplier_orders where id='{condition1}'""").fetchall()
                condition3 = number[0][0]
            if NotNull(condition2):
                date = engine.execute(f"""select date from supplier_orders where id='{condition1}'""").fetchall()
                condition2 = date[0][0]
            engine.execute(f"""update supplier_orders set date = '{condition2}', client = '{condition4}', 
                               cost = '{condition3}',executed = '{condition5}', number = {condition6} where id='{condition1}'""")
            if condition5 == 1:
                engine.execute(f"""update cash set cash = (select cost*(100 - (select percentage_price from suppliers where suppliers.id=
                    (select supplier from `supplier_orders` where supplier_orders.id={condition1})))/100 
                    from `supplier_orders` where supplier_orders.id={condition1}) where order_sup_id='{condition1}'""")
            flash("Order succesfully changed", category='error')
            mydb.commit()
            cursor.execute('SELECT * FROM {} ORDER BY 1'.format('supplier_orders'))
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return render_template("form15.html", table=records,
                                    columns=columns, title='Supplier Orders', id_first=True,)
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return render_template("table.html", table=records, columns=columns, title='Work', id_first=True,
                           length=len(records), defenition=defenit)


if __name__ == '__main__':
    lists_filling()
    app.run(debug=True)
