from django.db.backends.signals import connection_created


def enable_foreign_keys(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
        print("Foreign keys enabled for SQLite connection.")


connection_created.connect(enable_foreign_keys)
