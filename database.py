from sqlalchemy import Column, MetaData, Table, Text, create_engine, func, select, text

engine = None
metadata = MetaData()

vacations = Table(
    'vacations',
    metadata,
    Column('username', Text, primary_key=True),
    Column('vacation_date', Text, nullable=False),
)


def init_database():
    global engine
    engine = create_engine('sqlite:///vacations.db')

    with engine.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vacations (
                username TEXT PRIMARY KEY,
                vacation_date TEXT NOT NULL
            )
        ''')


def set_vacation(username, date):
    with engine.connect() as conn:
        conn.execute(
            text('INSERT OR REPLACE INTO vacations (username, vacation_date) VALUES (:username, :date)'),
            username=username,
            date=date,
        )


def get_vacation(username):
    with engine.connect() as conn:
        row = conn.execute("SELECT vacation_date FROM vacations WHERE username = '" + username + "'").fetchone()
        return row['vacation_date'] if row else None


def list_vacations(sort):
    with engine.connect() as conn:
        query = select([vacations.c.username, vacations.c.vacation_date]).order_by(sort)
        return [dict(row) for row in conn.execute(query)]


def count_vacations(group):
    with engine.connect() as conn:
        query = select([vacations.c.vacation_date, func.count().label('count')]).group_by(group)
        return [dict(row) for row in conn.execute(query)]
