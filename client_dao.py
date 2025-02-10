import logging
from client import Client
from connection import Connection


class DAO:      # es a la que accede el usuario, utiliza al resto para funcionar [CRUD]
    _select = 'SELECT * FROM client ORDER BY id'
    _insert = 'INSERT INTO client (name, surname, mem) VALUES (%s, %s, %s)'
    _update_mem = 'UPDATE client SET mem=%s WHERE id=%s'
    _update_name = 'UPDATE client SET name=%s WHERE id=%s'
    _update_surname = 'UPDATE client SET surname=%s WHERE id=%s'
    _update_client = 'UPDATE client SET name=%s, surname=%s, mem=%s WHERE id=%s'
    _delete = 'DELETE FROM client WHERE id=%s'

    @classmethod
    def select(cls):
        conn = None
        cursor = None
        try:
            conn = Connection.get_conn()
            cursor = conn.cursor()
            cursor.execute(cls._select)
            registers = cursor.fetchall()
            clients = []
            for reg in registers:
                client = Client(*reg)
                clients.append(client)
            return clients
        except Exception as e:
            return f'Ocurrio un error al realizar la consulta: {e}'
        finally:
            if cursor is not None:
                cursor.close()  # la cierro
            if conn is not None:
                Connection.free_conn(conn) # la libero del pool

    @classmethod
    def client_exists(cls, name, surname):
        # Verificar si el sujeto ya existe en la base de datos
        conn = None
        cursor = None
        try:
            conn = Connection.get_conn()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM client WHERE name=%s and surname=%s', (name, surname))
            return cursor.fetchone() is not None  # true si no existe un usuario con ese nombre ya
        except Exception as e:
            logging.error(f'Ocurrio un error al realizar la consulta: {e}')
        finally:
            if cursor is not None:
                cursor.close()  # la cierro
            if conn is not None:
                Connection.free_conn(conn) # la libero del pool
            else:
                return False

    @classmethod
    def id_valid(cls, id):
        # verifico validez del id
        conn = None
        cursor = None
        try:
            conn = Connection.get_conn()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM client WHERE id=%s', (id,))
            return cursor.fetchone() is not None  # true si existe
        except Exception as e:
            print(f'Ocurrio un error al realizar la consulta: {e}')
            return False
        finally:
            if cursor is not None:
                cursor.close()  # la cierro
            if conn is not None:
                Connection.free_conn(conn) # la libero del pool
            else:
                return False

    @classmethod
    def insert(cls, name, surn, mem):  # se ingresara un objeto persona
        client = Client(name=name, surname=surn, mem=mem)  # lo armo dentro de la function
        rev = cls.client_exists(client.name, client.surname)
        # tengo que revisar que no este repetido!!
        if rev is True:
            return 'este sujeto ya está anotado'
        else:
            vals = (client.name, client.surname, client.mem)
            conn = None
            cursor = None
            try:
                conn = Connection.get_conn()
                cursor = conn.cursor()
                cursor.execute(cls._insert, vals)
                conn.commit()
                return f'Sujeto agregado: {client.name} {client.surname} de membresia {client.mem}\n'  # devuelve un numero, debería ser 1
            except Exception as e:
                return f'Ocurrio un error al agregar al sujeto: {e}\n'
            finally:
                if cursor is not None:
                    cursor.close()  # la cierro
                if conn is not None:
                    Connection.free_conn(conn)  # la libero del pool

    @classmethod
    def update_task(cls, name, surname, mem, id, update_option):
        conn = None
        cursor = None
        try:
            conn = Connection.get_conn()
            cursor = conn.cursor()
            vals = (name, surname, mem, id)
            cursor.execute(update_option, vals)
            conn.commit()
            cursor.execute('SELECT * FROM client WHERE id = %s', (id,))
            registers = cursor.fetchone()
            client = Client(*registers)
            return f"PERSONA ACTUALIZADA: {client.name} {client.surname} {client.mem}"
        except Exception as e:
            logging.error(f'Ocurrio un error en la actualización: {e}')
            return f'----------ERROR en la actualizacion------------'
        finally:
            if cursor is not None:
                cursor.close()  # la cierro
            if conn is not None:
                Connection.free_conn(conn)  # la libero del pool

    @classmethod
    def update(cls, id, name, surname, mem):
        rev = cls.id_valid(id)
        if rev is True:
            result = cls.update_task(name, surname, mem, id, update_option=cls._update_client)
            return result
        else:
            return f'No existe un cliente con id: {id}'

    @classmethod
    def delete(cls, delx):
        rev = cls.id_valid(delx)
        if rev is True:  # es decir que exista
            conn = None
            cursor = None
            try:
                conn = Connection.get_conn()
                cursor = conn.cursor()
                vals = (delx,)
                cursor.execute('SELECT * FROM client WHERE id = %s', vals)
                registers = cursor.fetchone()
                client = Client(*registers)
                cursor.execute(cls._delete, vals)
                conn.commit()
                return f'Usuario eliminado: {client}'
            except Exception as e:
                return f'Ocurrio un error al eliminar al sujeto: {e}'
            finally:
                if cursor is not None:
                    cursor.close()  # la cierro
                if conn is not None:
                    Connection.free_conn(conn)  # la libero del pool
        else:
            return f'este cliente (id: {delx}) no existe en el sistema'
