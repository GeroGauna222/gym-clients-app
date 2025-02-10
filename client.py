class Client:  # tiene una funcion dada; la creacion de sujetos, y nada mas, son los que se ingresarán
    def __init__(self, id=None, name=None, surname=None, mem=None):
        self._id = id  # NO SE LO VOY A INGRESAR NUNCA
        self._name = name
        self._surname = surname
        self._mem = mem

    def __str__(self):
        return f'''
        [ID: {self._id}]
        [NAME: {self._name}]
        [SURNAME: {self._surname}]
        [MEMBERSHIP: {self._mem}]
    '''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, s):
        self._surname = s

    @property
    def mem(self):
        return self._mem
    @mem.setter
    def mem(self, m):
        self._mem = m

