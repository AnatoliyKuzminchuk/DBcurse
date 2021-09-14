import mysql.connector

"""Function for table creating autoparts_store."""


def create_suppliers(engine):
    """Suppliers table creating"""
    engine.execute("""
                   create table Suppliers(
                       id integer primary key auto_increment,  # PK
                       name varchar(30),  # name of supplier
                       country varchar(30),  # name of supplier's country
                       type varchar(15),  # type of supplier
                       time_of_delivery integer,  # delivery time in days
                       percentage_price integer  # part of cash which come back to supplier
                   )
    """)


def create_catalog(engine):
    """Catalog table creating"""
    engine.execute("""
                   create table Catalog(
                        id integer primary key auto_increment,  # PK
                        name varchar(30) unique,  # name of detail
                        price integer,  # the price of detail
                        size integer  # how much place took this detail in section
                   )
    """)


def create_warehouse_sections(engine):
    """Warehouse_Sections table creating"""
    engine.execute("""
                    create table Warehouse_Sections(
                        id integer primary key auto_increment,  # PK
                        alias varchar(30),  # naming of section
                        part_type integer,  # FK to Catalog; match detail with Catalog
                        total_size integer,  # size of the section
                        foreign key (part_type) references Catalog (id)
                   )
    """)


def create_warehouse(engine):
    """Warehouse table creating"""
    engine.execute("""
                    create table warehouse(
                        id integer primary key auto_increment,  # PK 
                        section integer,  # FK to Warehouse_Sections
                        number integer,  # number of this details in the stock
                        supplier integer,  # FK to Suppliers
                        date Date,  # coming time
                        foreign key (section) references Warehouse_Sections (id),
                        foreign key (supplier) references Suppliers (id)
                   )
    """)


def create_client(engine):
    """Створити таблицю з інформацією, щодо користувачів"""
    engine.execute("""
                    create table Clients(
                        id integer primary key auto_increment,  # PK
                        name varchar(30) unique,  # first&second client's names
                        password varchar(30),  # client's password
                        phone varchar(15)  # client's phone number
                   )
    """)


def create_warehouse_orders(engine):
    """Warehouse_Orders table creating."""
    engine.execute("""
                    create table Warehouse_Orders(
                        id integer primary key auto_increment,  # PK
                        date Date,  # date of order 
                        client integer,  # FK to Clients_Base
                        part integer,  # FK to Catalog
                        section integer,  # FK to Warehouse_Sections
                        number integer,  # number of parts
                        supplier integer,  # FK to Suppliers
                        cost integer, # cost of delivery
                        foreign key (client) references Clients (id),  
                        foreign key (part) references Catalog (id),
                        foreign key (section) references Warehouse_Sections (id),
                        foreign key (supplier) references Suppliers (id)
                   )
    """)


def create_supplier_orders(engine):
    """Supplier_Orders table creating"""
    engine.execute("""
                    create table Supplier_Orders(
                        id integer primary key auto_increment,  # PK
                        date Date,  # date of creating order
                        client integer default null,  # FK to Clients_Base
                        part integer,  # FK to Catalog
                        executed bool default false,  # True if order was executed, else False
                        number integer,  # number of details
                        supplier integer,  # FK to Suppliers
                        cost integer, # cost of delivery
                        foreign key (client) references Clients (id), 
                        foreign key (part) references Catalog (id), 
                        foreign key (supplier) references Suppliers (id)
                    ) 
    """)


def create_overheads(engine):
    """Overhead table creating"""
    engine.execute("""
                    create table Overheads(
                        id integer primary key auto_increment,  # PK
                        type varchar(20),  # тип накладного расхода
                        explanation varchar(40),  # дополнительные пояснения по поводу накладного расхода
                        date Date,  # date of spending money
                        money integer  # amount of money
                    ) 
    """)


def create_defects(engine):
    """Defects table creating"""
    engine.execute("""
                    create table Defects(
                        id integer primary key auto_increment,  # PK
                        date Date,  # date the entry was created
                        part integer,   # FK to Catalog
                        supplier integer,  # FK to Suppliers
                        number integer,  # number of defect parts
                        cost integer, # return cost
                        foreign key (part) references Catalog (id),
                        foreign key (supplier) references Suppliers (id)
                    ) 
    """)


def create_cash_count(engine):
    """Cash table creating."""
    engine.execute("""
                    create table Cash(
                        id integer primary key auto_increment,  # PK
                        cash integer, 
                        date date,
                        overhead_id integer null, # FK to overhead
                        order_sup_id integer null,  # FK to supplier_order
                        order_war_id integer null,  # FK to warehouse_order
                        defects_id integer null,  # FK to Defects
                        foreign key (overhead_id) references Overheads (id),
                        foreign key (order_sup_id) references Supplier_Orders (id),
                        foreign key (order_war_id) references Warehouse_Orders (id),
                        foreign key (defects_id) references Defects (id)
                    ) 
    """)


def full_create(engine, *args):
    """Create dll tables"""
    create_suppliers(engine)
    create_catalog(engine)
    create_warehouse_sections(engine)
    create_warehouse(engine)
    create_client(engine)
    create_warehouse_orders(engine)
    create_supplier_orders(engine)
    create_overheads(engine)
    create_defects(engine)
    create_cash_count(engine)


def full_drop(engine, *args):
    """Database clearing"""
    engine.execute("""drop table if exists Cash""")
    engine.execute("""drop table if exists Defects""")
    engine.execute("""drop table if exists Overheads""")
    engine.execute("""drop table if exists Supplier_Orders""")
    engine.execute("""drop table if exists Warehouse_Orders""")
    engine.execute("""drop table if exists Clients""")
    engine.execute("""drop table if exists Warehouse""")
    engine.execute("""drop table if exists Warehouse_Sections""")
    engine.execute("""drop table if exists Catalog""")
    engine.execute("""drop table if exists Suppliers""")


if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL2021",
        database="autoparts_store"
    )

    my_engine = mydb.cursor()
    full_drop(my_engine)
    full_create(my_engine)
