import mysql.connector
from mysql.connector import pooling


class Connection:
    _HOST = "localhost"
    _USER = "root"
    _PASSWORD = "admin"
    _DATABASE = "zona_fit_db"
    _POOL_SIZE = 5
    _POOL_NAME = "zona_fit_db_pool"
    _DB_PORT = 3306
    pool = None

    @classmethod
    def get_pool(cls):  # lo utiliza get_conn
        if cls.pool is None:
            try:
                cls.pool = pooling.MySQLConnectionPool(
                    pool_name=cls._POOL_NAME,
                    pool_size=cls._POOL_SIZE,
                    host=cls._HOST,
                    user=cls._USER,
                    password=cls._PASSWORD,
                    database=cls._DATABASE,
                    port=cls._DB_PORT
                )
                print(f'Pool creado con exito: {cls.pool}')
                return cls.pool
            except Exception as e:
                print(f'Ocurrio un error al obtener el pool: {e}')
        else:
            return cls.pool

    @classmethod
    def get_conn(cls):
        pool = cls.get_pool()
        conn = pool.get_connection()
        return conn

    @classmethod
    def free_conn(cls, conn):
        conn.close()