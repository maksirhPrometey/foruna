"""PyMySQL як драйвер MySQLdb — для shared hosting без mysqlclient."""


def install_pymysql() -> None:
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
