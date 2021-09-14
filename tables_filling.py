"""Functions to tables filling"""

def insert_suppliers(engine, name, country='Ukraine', supplier_type='dealer',
                                 time_of_delivery=1, percentage_price=80):
    """Insert new row to Suppliers."""

    engine.execute(f"""insert into Suppliers (name, country, type, time_of_delivery, percentage_price) 
                   values ('{name}', '{country}', '{supplier_type}', '{time_of_delivery}', '{percentage_price}')""")

def filling_suppliers(engine):
    """Filling data into Supplier"""
    insert_suppliers(engine, 'NukaWorld', 'Los Angeles', 'dealer', 1, 80)
    insert_suppliers(engine, 'Kuata Shipyards', 'Kuat', 'large firm', 4, 50)
    insert_suppliers(engine, '4x4', 'Marvel', 'small firm', 1, 85)
    insert_suppliers(engine, 'Tree', 'Japan', 'small firm', 9, 40)
    insert_suppliers(engine, 'Rothana Heavy Engineering', 'Rothana', 'dealer', 1, 80)
    insert_suppliers(engine, 'Stark Indastries', 'Marvel', 'large firm', 4, 90)
    insert_suppliers(engine, 'Uein Indastries', 'USA', 'dealer', 13, 50)
    insert_suppliers(engine, 'Orcheim tribal', 'Russia', 'dealer', 2, 25)
    insert_suppliers(engine, 'Ave Cesaer', 'Rome', 'large firm', 1, 45)
    insert_suppliers(engine, 'Gulag', 'Sibyr', 'dealer', 1, 95)
    insert_suppliers(engine, 'SS', 'Germany', 'large firm', 1, 85)
    insert_suppliers(engine, 'Galactic Republic', 'FarFarAway', 'dealer', 1, 75)


def insert_catalog(engine, name, price, part_size=1):
    """Insert new row to Catalog."""
    engine.execute(f"insert into Catalog (name, price, size) values ('{name}', '{price}', '{part_size}')")


def filling_catalog(engine):
    """Заполняет данными таблицу Catalog."""
    insert_catalog(engine, 'Blaster', 200, 4)
    insert_catalog(engine, 'Babaha', 400, 1)
    insert_catalog(engine, 'Big blaster', 700, 2)
    insert_catalog(engine, 'Horror drop', 1000, 1)
    insert_catalog(engine, 'Killer Bee', 2020, 1)
    insert_catalog(engine, 'Licence', 4000, 1)
    insert_catalog(engine, 'Slaks', 4500, 3)
    insert_catalog(engine, 'Tires', 850, 1)
    insert_catalog(engine, 'Clone from Camino', 10000, 2)
    insert_catalog(engine, 'Step part', 6050, 2)
    insert_catalog(engine, 'Iron men', 12500, 2)
    insert_catalog(engine, 'Skaiwoker sword', 20000, 1)
    insert_catalog(engine, 'Star Killer eye', 30000, 5)


def insert_warehouse_sections(engine, alias, part_type, total_size):
    """Insert new row to Warehouse_Sections."""
    engine.execute(f"""insert into Warehouse_Sections (alias, part_type, total_size) 
                    values ('{alias}', '{part_type}', '{total_size}')""")


def filling_warehouse_sections(engine):
    """Заполняет данными таблицу Warehouse_Sections."""
    insert_warehouse_sections(engine, 'A section', 1, 4000)
    insert_warehouse_sections(engine, 'B section', 1, 4000)
    insert_warehouse_sections(engine, 'C section', 1, 4000)
    insert_warehouse_sections(engine, 'D section', 2, 4000)
    insert_warehouse_sections(engine, 'E section', 3, 8000)
    insert_warehouse_sections(engine, 'F section', 4, 8000)
    insert_warehouse_sections(engine, 'G section', 5, 8000)
    insert_warehouse_sections(engine, 'H section', 6, 8000)
    insert_warehouse_sections(engine, 'J section', 7, 13000)
    insert_warehouse_sections(engine, 'F section', 8, 13000)
    insert_warehouse_sections(engine, 'R section', 9, 13000)
    insert_warehouse_sections(engine, 'K section', 10, 13000)
    insert_warehouse_sections(engine, 'L section', 11, 3000)
    insert_warehouse_sections(engine, 'M section', 12, 3000)
    insert_warehouse_sections(engine, 'N section', 13, 3000)


def insert_warehouse(engine, section, number, supplier, date):
    """Insert new row to Warehouse."""
    engine.execute(f"""insert into Warehouse (section, number, supplier, date) values ('{section}', '{number}', '{supplier}', 
                    '{date}')""")

# insert_warehouse(engine, section, number, supplier, date)
def filling_warehouse(engine):
    """Заполняет данными таблицу Warehouse."""
    insert_warehouse(engine, 1, 1, 4, '2019-03-04')
    insert_warehouse(engine, 1, 3, 1, '2019-03-04')
    insert_warehouse(engine, 2, 30, 1, '2020-03-04')
    insert_warehouse(engine, 3, 26, 3, '2020-05-04')
    insert_warehouse(engine, 3, 45, 4, '2020-06-04')
    insert_warehouse(engine, 5, 37, 2, '2019-07-14')
    insert_warehouse(engine, 6, 36, 7, '2020-08-24')
    insert_warehouse(engine, 4, 46, 5, '2019-09-04')
    insert_warehouse(engine, 7, 43, 5, '2020-11-14')
    insert_warehouse(engine, 8, 32, 5, '2019-11-28')
    insert_warehouse(engine, 9, 103, 5, '2020-12-28')
    insert_warehouse(engine, 10, 13, 7, '2021-01-13')
    insert_warehouse(engine, 11, 11, 2, '2020-01-13')
    insert_warehouse(engine, 12, 15, 2, '2020-01-13')
    insert_warehouse(engine, 13, 34, 5, '2021-03-15')
    insert_warehouse(engine, 14, 10, 2, '2020-05-17')
    insert_warehouse(engine, 15, 2, 5, '2020-01-18')
    insert_warehouse(engine, 14, 15, 6, '2021-01-21')
    insert_warehouse(engine, 10, 3, 7, '2021-01-25')
    insert_warehouse(engine, 10, 4, 2, '2020-02-03')


def insert_clients(engine, name, password, phone):
    """Insert new row to Clients."""
    engine.execute(f"insert into Clients (name, password, phone) values ('{name}', '{password}', '{phone}')")


def filling_clients_base(engine):
    """Заполняет данными таблицу Clients_Base."""
    insert_clients(engine, 'YOURSELF', 'qwerty', '+000-000-000-00')
    insert_clients(engine, 'Anakin Skywalker', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Luke Skywalker', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Leia Organa', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Han Solo', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Ben Solo', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Padme Amidala', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Jobal Naberrie', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Pooja Naberrie', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Ruwee Naberrie', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Ryoo Naberrie', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Sola Naberrie', 'qwerty', '+259-150-242-20')
    insert_clients(engine, 'Beru Whitesun Lars', 'qwerty', '+259-150-242-21')
    insert_clients(engine, 'Cliegg Lars', 'qwerty', '+259-150-242-22')
    insert_clients(engine, 'Owen Lars', 'qwerty', '+259-150-242-23')
    insert_clients(engine, 'Aika Lars', 'qwerty', '+259-150-242-24')
    insert_clients(engine, 'Bail Organa', 'qwerty', '+259-150-242-25')
    insert_clients(engine, 'Breha Organa', 'qwerty', '+259-150-242-26')
    insert_clients(engine, 'Avar Kriss', 'qwerty', '+259-150-242-27')
    insert_clients(engine, 'Depa Billaba', 'qwerty', '+259-150-242-28')
    insert_clients(engine, 'Shmi Skywalker', 'qwerty', '+259-150-242-29')
    insert_clients(engine, 'Ezra Bridger', 'qwerty', '+259-150-242-36')
    insert_clients(engine, 'Eno Cordova', 'qwerty', '+259-150-242-14')
    insert_clients(engine, 'Cin Drallig', 'shine', '+259-150-242-12')
    insert_clients(engine, 'Sifo-Dyas', 'shine', '+259-150-242-04')
    insert_clients(engine, 'Caleb Dume', 'shine', '+259-150-242-44')
    insert_clients(engine, 'Qui-Gon Jinn', 'shine', '+259-150-242-54')
    insert_clients(engine, 'Cere Junda', 'shine', '+259-150-242-84')
    insert_clients(engine, 'Ben Kenobi', 'shine', '+259-150-242-94')
    insert_clients(engine, 'Cal Kestis', 'shine', '+259-150-242-53')
    insert_clients(engine, 'Jocasta Nu', 'shine', '+259-150-242-91')


def insert_warehouse_orders(engine, date, client, part, section, number, supplier):
    """Insert new row to Warehouse_Orders."""
    engine.execute(f"""insert into Warehouse_Orders (date, client, part, section, number, supplier, cost)
                   values ('{date}', '{client}', '{part}', '{section}', '{number}', '{supplier}',
                   (select price*'{number}'  from catalog where  catalog.id = '{part}'))""")
    insert_cash(engine, 'warehouse_orders')


# insert_warehouse_orders(engine, date, client, part, section, number, supplier)
def filling_warehouse_orders(engine):
    """Заполняет данными таблицу Warehouse_Orders."""
    insert_warehouse_orders(engine, '2019-03-07', 7, 8, 10, 13, 6)
    insert_warehouse_orders(engine, '2021-01-25', 11, 3, 5, 24, 7)
    insert_warehouse_orders(engine, '2021-03-04', 12, 1, 1, 35, 8)
    insert_warehouse_orders(engine, '2020-05-04', 12, 5, 7, 14, 9)
    insert_warehouse_orders(engine, '2021-06-04', 13, 8, 10, 3, 10)
    insert_warehouse_orders(engine, '2019-07-14', 8, 6, 8, 21, 10)
    insert_warehouse_orders(engine, '2020-08-24', 13, 8, 10, 23, 11)
    insert_warehouse_orders(engine, '2019-09-04', 7, 3, 5, 19, 11)


def insert_supplier_orders(engine, date, client, part, executed, number, supplier):
    """Insert new row to Supplier_Orders."""
    engine.execute(f"""insert into Supplier_Orders (date, client, part, executed, number, supplier, cost)
                   values ('{date}', '{client}', '{part}', '{executed}', '{number}', '{supplier}',
                   (select price  from catalog where  catalog.id = '{part}')*'{number}')""")
    exe = engine.execute(f"""select executed from supplier_orders where 
                                id = (SELECT LAST_INSERT_ID())""").fetchall()
    exe = exe[0][0]
    if exe == 1:
        insert_cash(engine, 'supplier_orders_ex')
    if exe == 0:
        insert_cash(engine, 'supplier_orders_not_ex')


# insert_supplier_orders(engine, date, client, part, executed, number, supplier)
def filling_supplier_orders(engine):
    """Заполняет данными таблицу Warehouse_Orders."""
    insert_supplier_orders(engine, '2019-03-03', 1, 1, '1', 12, 4)
    insert_supplier_orders(engine, '2019-03-03', 1, 1, '1', 3, 1)
    insert_supplier_orders(engine, '2019-03-03', 1, 1, '1', 30, 1)
    insert_supplier_orders(engine, '2019-05-03', 1, 1, '1', 26, 3)
    insert_supplier_orders(engine, '2019-06-03', 1, 1, '1', 85, 4)
    insert_supplier_orders(engine, '2019-09-03', 1, 2, '1', 46, 5)
    insert_supplier_orders(engine, '2019-06-13', 1, 3, '1', 37, 2)
    insert_supplier_orders(engine, '2019-08-23', 1, 4, '1', 36, 7)
    insert_supplier_orders(engine, '2019-11-13', 1, 5, '1', 53, 5)
    insert_supplier_orders(engine, '2019-12-27', 1, 6, '1', 32, 5)
    insert_supplier_orders(engine, '2019-12-27', 1, 7, '1', 113, 5)
    insert_supplier_orders(engine, '2021-01-12', 1, 8, '1', 13, 7)
    insert_supplier_orders(engine, '2021-01-24', 1, 8, '1', 3, 7)
    insert_supplier_orders(engine, '2021-02-02', 1, 8, '1', 4, 2)
    insert_supplier_orders(engine, '2021-01-12', 1, 9, '1', 11, 2)
    insert_supplier_orders(engine, '2021-01-12', 1, 10, '1', 15, 2)
    insert_supplier_orders(engine, '2021-01-14', 1, 11, '1', 34, 5)
    insert_supplier_orders(engine, '2021-01-16', 1, 12, '1', 10, 2)
    insert_supplier_orders(engine, '2021-01-20', 1, 12, '1', 15, 6)
    insert_supplier_orders(engine, '2020-01-17', 1, 13, '1', 2, 5)
    insert_supplier_orders(engine, '2019-03-03', 7, 8, '1', 75, 6)
    insert_supplier_orders(engine, '2020-01-12', 11, 3, '1', 64, 7)
    insert_supplier_orders(engine, '2019-12-27', 12, 1, '1', 35, 8)
    insert_supplier_orders(engine, '2020-01-17', 12, 5, '1', 64, 9)
    insert_supplier_orders(engine, '2020-03-04', 13, 8, '1', 53, 10)
    insert_supplier_orders(engine, '2020-05-04', 8, 6, '1', 32, 10)
    insert_supplier_orders(engine, '2020-06-04', 13, 8, '1', 53, 11)
    insert_supplier_orders(engine, '2019-07-14', 7, 3, '1', 35, 11)
    insert_supplier_orders(engine, '2020-08-24', 18, 7, '0', 3, 11)
    insert_supplier_orders(engine, '2019-09-04', 8, 9, '0', 42, 12)
    insert_supplier_orders(engine, '2020-11-14', 1, 1, '1', 7, 4)
    insert_supplier_orders(engine, '2019-11-28', 12, 5, '1', 4, 9)


def insert_overheads(engine, overhead_type, explanation, date, money):
    """Insert new row to Overheads."""
    engine.execute(f"""insert into Overheads (type, explanation, date, money) 
                   values ('{overhead_type}', '{explanation}', '{date}', '{money}')""")
    insert_cash(engine, type='overhead')


# insert_overheads(engine, overhead_type, explanation, date, money)
def filling_overheads(engine):
    """Заполняет данными таблицу Overheads."""
    insert_overheads(engine, 'Salary', '', '2020-03-03', 5000)
    insert_overheads(engine, 'Drunk', '', '2020-04-03', 15000)
    insert_overheads(engine, 'Sluts', '', '2020-05-03', 30000)


def insert_defects_register(engine, date, part, supplier, number):
    """Insert new row to Defects_Register."""
    engine.execute(f"""insert into Defects (date, part, supplier, number, cost)
                   values ('{date}', '{part}', '{supplier}', '{number}',
                   (select price*'{number}'  from catalog where  catalog.id = '{part}'))""")
    insert_cash(engine, type='defect')


# insert_defects_register(engine, date, part, supplier, number)
def filling_defects(engine):
    """Insert new row to Defects."""
    insert_defects_register(engine, '2019-03-03', 1, 4, 2)
    insert_defects_register(engine, '2020-01-17',  5,  9, 4)


def insert_cash(engine, type):
    """Insert new row to Cash."""
    if type == 'overhead':
        engine.execute(f"""insert into Cash (overhead_id, cash, date) values ((SELECT LAST_INSERT_ID()), 
                       (select -money from overheads where overheads.id=(SELECT LAST_INSERT_ID())),
                       (select date from overheads where overheads.id=(SELECT LAST_INSERT_ID())))""")
    if type == 'warehouse_orders':
        engine.execute(f"""insert into Cash (order_war_id, cash, date) values ((SELECT LAST_INSERT_ID()), 
                       (select cost*(100 - (select percentage_price from suppliers where suppliers.id=
                    (select supplier from `warehouse_orders` where warehouse_orders.id=(SELECT LAST_INSERT_ID()))))/100
                     from `warehouse_orders` where warehouse_orders.id=(SELECT LAST_INSERT_ID())),
                    (select date from `warehouse_orders` where warehouse_orders.id=(SELECT LAST_INSERT_ID())))""")
    if type == 'supplier_orders_ex':
        engine.execute(f"""insert into Cash (order_sup_id, cash, date) values ((SELECT LAST_INSERT_ID()), 
                    (select cost*(100 - (select percentage_price from suppliers where suppliers.id=
                    (select supplier from `supplier_orders` where supplier_orders.id=(SELECT LAST_INSERT_ID()))))/100 
                    from `supplier_orders` where supplier_orders.id=(SELECT LAST_INSERT_ID())), 
                    (select date from `supplier_orders` where supplier_orders.id=(SELECT LAST_INSERT_ID())));""")
    if type == 'supplier_orders_not_ex':
        engine.execute(f"""insert into Cash (order_sup_id, date) values ((SELECT LAST_INSERT_ID()), 
                        (select date from `supplier_orders` where supplier_orders.id=(SELECT LAST_INSERT_ID())))""")
    if type == 'defect':
        engine.execute(f"""insert into Cash (defects_id, cash, date) values ((SELECT LAST_INSERT_ID()), 
                        (select -cost from `defects` where defects.id=(SELECT LAST_INSERT_ID())),
                        (select date from `defects` where defects.id=(SELECT LAST_INSERT_ID())))""")



def filling_tables(engine, *args):
    """Filling all tables."""
    filling_suppliers(engine)
    filling_catalog(engine)
    filling_warehouse_sections(engine)
    filling_warehouse(engine)
    filling_clients_base(engine)
    filling_warehouse_orders(engine)
    filling_supplier_orders(engine)
    filling_overheads(engine)
    filling_defects(engine)


if __name__ == '__main__':
    from sqlalchemy import create_engine

    my_engine = create_engine('mysql+pymysql://root:MySQL2021@localhost:3306/autoparts_store')

    filling_tables(my_engine)
