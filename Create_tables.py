import os.path

from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from clickhouse_driver import Client

from .tables import Base, User, Operation


class DatabaseCreate:
    is_exists_db: bool
    url: str
    is_clickhouse: bool
    is_sqlite: bool
    is_mysql: bool
    is_postgres: bool

    def __init__(self, url):
        self.url = url
        self.is_exists_db = False
        self.is_sqlite = False
        self.is_mysql = False
        self.is_postgresql = False
        self.is_clickhouse = False


    def check_if_sqlite(self):
        if (self.url == 'sqlite:///./database003.sqlite3'):
            self.is_sqlite = True


    def check_if_mysql(self):
        if (self.url == 'mysql+pymysql://root:1111@localhost/database1'):
            self.is_mysql = True


    def check_if_postgresql(self):
        if (self.url == 'postgresql+psycopg2://postgres:1111@localhost/database005'):
            self.is_postgresql = True


    def check_if_clickhouse(self):
        if (self.url == 'clickhouse+native://default:@localhost:9000/default'):
            self.is_clickhouse = True


    def check_db(self):
        if os.path.exists('.env'):
            with open('.env', "r") as file:
                line = file.readline().rstrip()
                self.url = line[13:]

                self.check_if_sqlite()
                self.check_if_mysql()
                self.check_if_postgresql()
                self.check_if_clickhouse()


                if self.is_sqlite:
                    if os.path.exists('database003.sqlite3'):
                        print("База данных SQLite существует")
                        self.is_exists_db = True
                    else:
                        print("Базы данных SQLite не существует")
                        self.is_exists_db = False
                elif self.is_mysql:
                    if database_exists(self.url):
                        print("База данных MySQL существует")
                        self.is_exists_db = True
                    else:
                        print("Базы данных MySQL не существует")
                        self.is_exists_db = False
                elif self.is_postgresql:
                    if database_exists(self.url):
                        print("База данных PostgreSQL существует")
                        self.is_exists_db = True
                    else:
                        print("Базы данных PostgreSQL не существует")
                        self.is_exists_db = False
                elif self.is_clickhouse:
                    if database_exists(self.url):
                        print("База данных ClickHouse существует")
                        self.is_exists_db = True
                    else:
                        print("База данных ClickHouse не существует")
                        self.is_exists_db = False


    def insert_data(self, engine):
        u1 = User(
            email='email.@examle.com',
            username='alex',
            password_hash='$2b$12$QrQtOwRLTtpNXhTCaewOtemyeesWHE8Ps04U.UEI62520lDQS2QUy'
        )

        o1 = Operation(
            date='19.02.2024',
            kind='income',
            amount=250.00,
            description='None'
        )
        o2 = Operation(
            date='20.02.2024',
            kind='income',
            amount=150.00,
            description='None'
        )
        o3 = Operation(
            date='20.02.2024',
            kind='outcome',
            amount=100.00,
            description='None'
        )
        o4 = Operation(
            date='21.02.2024',
            kind='outcome',
            amount=50.00,
            description='None'
        )
        o5 = Operation(
            date='21.02.2024',
            kind='income',
            amount=25.00,
            description='None'
        )


        u1.operation.extend([o1, o2, o3, o4, o5])

        session = sessionmaker(bind=engine)
        session = Session(bind=engine)
        session.add(u1)
        session.commit()

        session.add_all([o1, o2, o3, o4, o5])
        session.commit()
        session.close()


    def create_db(self):
        if not self.is_exists_db:
            print("Создаем БД")
            if not self.is_clickhouse:
                create_database(self.url)
                engine = create_engine(self.url)
                Base.metadata.create_all(engine)
                self.insert_data(engine)
            else:
                client = Client('localhost')

                # Создание базы данных
                client.execute('CREATE DATABASE IF NOT EXISTS default')

                # Создание таблицы 1
                client.execute('''
                    CREATE TABLE IF NOT EXISTS default.users (
                        id Int32,
                        email String,
                        username String,
                        password_hash String,
                    ) ENGINE = MergeTree()
                    ORDER BY id
                ''')

                # Создание таблицы 2
                client.execute('''
                    CREATE TABLE IF NOT EXISTS default.operations (
                        id Int32,
                        user_id Int32,
                        date String,
                        kind String,
                        amount Float64,
                        description String,
                    ) ENGINE = MergeTree()
                    ORDER BY id
                ''')

                # Вставка данных в таблицы

                client.execute('INSERT INTO users (id, email, username, password_hash) VALUES',
                               [(1, 'user1@example.com', 'user1',
                                 '$2b$12$QrQtOwRLTtpNXhTCaewOtemyeesWHE8Ps04U.UEI62520lDQS2QUy')])
                client.execute('INSERT INTO operations (id, user_id, date, kind, amount, description) VALUES',
                               [(3, 1, '2022-01-01', 'income', 200.0, 'Initial deposit2'),
                                (4, 1, '20   22-01-02', 'outcome', 250.0, 'ATM withdrawal2')])

                # Вывод данных из таблиц
                print(client.execute('SHOW TABLES'))
                result_operations = client.execute('SELECT * FROM operations')
                print(result_operations)
                result_users = client.execute('SELECT * FROM users')
                print(result_users)




