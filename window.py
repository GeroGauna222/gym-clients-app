import client_dao
import tkinter
from tkinter import ttk, messagebox
from client_dao import DAO

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()  # me trae el constructor de la clase padre (Tk)
        # configuracion del window y los frames
        self.win_config()
        self.f_tit = ttk.Frame(self)
        self.f_tit_config()
        self.f_table = ttk.Frame(self)
        self.f_table_config()
        self.f_search = ttk.Frame(self)
        self.f_search_config()
        self.f_buttons = ttk.Frame(self)
        self.f_buttons_config()
        self.id_now = None

        # Table Frame
        # table widg
        cols = ('ID', 'Name', 'Surname', 'Membership')
        self.table = ttk.Treeview(self.f_table, columns=cols, show='headings')

        clients = DAO.select()
        for client in clients:
            self.table.insert(parent='', index=tkinter.END, values=(client.id, client.name, client.surname, client.mem))
        self.table_config()

        # scrollbar
        self.bar = ttk.Scrollbar(self.f_table, orient=tkinter.VERTICAL, command=self.table.yview)
        self.scrollbar_config()

        # Search Frame and Title
        self.labels()
        self.entries()

        # Buttons
        self.btts()

        # style
        self.sty = ttk.Style()
        self.style_config()

    def win_config(self):
        self.title('ZonaFit')
        self.iconbitmap('loginico.ico')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=2)
        self.configure(background='white', relief='sunken')
        self.geometry('700x500')

    def f_tit_config(self):
        self.f_tit.columnconfigure(0, weight=1)
        self.f_tit.rowconfigure(0, weight=1)
        self.f_tit.grid(row=0, column=0, sticky='NSWE', columnspan=2)

    def f_table_config(self):
        self.f_table.columnconfigure(0, weight=1)
        self.f_table.columnconfigure(1, weight=0)
        self.f_table.rowconfigure(0, weight=1)
        self.f_table.grid(row=1, column=1, sticky='NSWE')

    def f_search_config(self):
        self.f_search.columnconfigure(0, weight=1)
        self.f_search.columnconfigure(1, weight=4)
        self.f_search.rowconfigure(0, weight=1)
        self.f_search.rowconfigure(1, weight=1)
        self.f_search.rowconfigure(2, weight=1)
        self.f_search.grid(row=1, column=0, sticky='NSWE')

    def f_buttons_config(self):
        self.f_buttons.columnconfigure(0, weight=1)
        self.f_buttons.columnconfigure(1, weight=1)
        self.f_buttons.columnconfigure(2, weight=1)
        self.f_buttons.rowconfigure(0, weight=1)
        self.f_buttons.grid(row=2, column=0, columnspan=2, sticky='NSWE')

    # @staticmethod
    # def insert_data(ppl, tab):
    #     for data in ppl:
    #         tab.insert(parent='', index=tkinter.END, values=data)
    #         # no tiene padre (tabla no en formato arbol), se agrega ultimo, el valor data (cada tupla en la tupla)

    # para el select en la tabla

    def clean_data(self):
        pass

    def reload_data(self):
        self.table.delete(*self.table.get_children())  # ver bien a fondo como funciona esta linea de codigo
        clients = DAO.select()
        for client in clients:
            self.table.insert(parent='', index=tkinter.END, values=(client.id, client.name, client.surname, client.mem))

    def show_reg(self, event):
        self.select = self.table.selection()
        if self.select:
            sel = self.table.item(self.select)
            client = sel['values']
            messagebox.showinfo(title='Info', message=f'[ID]: [{client[0]}]\n[Name]: [{client[1]}]\n[Surname]: [{client[2]}]\n'
                                                      f'[Membership]: [{client[3]}]\n')
            self.id_now = client[0]
            self.n_s.set(client[1])
            self.sn_s.set(client[2])
            self.m_s.set(client[3])

    def table_config(self):
        self.table.heading('ID', text='ID', anchor=tkinter.CENTER)
        self.table.heading('Name', text='Name')
        self.table.heading('Surname', text='Surname')
        self.table.heading('Membership', text='Membership')
        self.table.column('ID', width=3)
        self.table.column('Surname', width=40)
        self.table.column('Name', width=40)
        self.table.column('Membership', width=15)
        # Ingreso datos a la tabla
        # App.insert_data(self.data_ppl, self.table)
        # funcionalidad (select)
        self.table.bind('<<TreeviewSelect>>', lambda e: self.show_reg(e))
        # lo inserto
        self.table.grid(row=0, column=0, sticky='NSWE')

    def scrollbar_config(self):
        self.table.configure(yscrollcommand=self.bar.set)
        self.bar.grid(row=0, column=1, sticky='NS')

    def style_config(self):
        self.sty.theme_use('clam')
        self.sty.configure('Treeview', background='black', foreground='white', fieldbackground='black')
        self.sty.map('Treeview', background=[('selected', '#3a86ff')])

    def labels(self):
        lab_n = ttk.Label(self.f_search, text='Name:')
        lab_s = ttk.Label(self.f_search, text='Surname:')
        lab_m = ttk.Label(self.f_search, text='Membership:')
        lab_s.grid(row=1, column=0)
        lab_n.grid(row=0, column=0, sticky='S')
        lab_m.grid(row=2, column=0, sticky='N')
        lab_tit = ttk.Label(self.f_tit, text='ZONA FIT GYM')
        lab_tit.configure(anchor='center', font=('Times New Roman', 18, 'bold'))
        lab_tit.grid(row=0, column=0)

    @staticmethod
    def clear_entry(event, entry, placeholder, case):
        if entry.get() == placeholder:
            entry.delete(0, tkinter.END)
        if case == 1:
            entry.config(show='*')

    def entries(self):
        self.n_s = tkinter.StringVar(value='Insert name')
        entry_n_s = ttk.Entry(self.f_search, width=10, textvariable=self.n_s)
        entry_n_s.bind('<FocusIn>', lambda e: App.clear_entry(event=e, entry=entry_n_s,
                                                              placeholder='Insert name', case=0))
        entry_n_s.grid(column=1, row=0, padx=10, pady=0, sticky='SEW')

        self.sn_s = tkinter.StringVar(value='Insert surname')
        entry_sn_s = ttk.Entry(self.f_search, width=10, textvariable=self.sn_s)
        entry_sn_s.bind('<FocusIn>', lambda e: App.clear_entry(event=e, entry=entry_sn_s,
                                                               placeholder='Insert surname', case=0))
        entry_sn_s.grid(column=1, row=1, padx=10, pady=0, sticky='EW')

        self.m_s = tkinter.StringVar(value='Insert membership')
        entry_m_s = ttk.Entry(self.f_search, width=10, textvariable=self.m_s)
        entry_m_s.bind('<FocusIn>', lambda e: App.clear_entry(event=e, entry=entry_m_s,
                                                              placeholder='Insert membership', case=0))
        entry_m_s.grid(column=1, row=2, padx=10, pady=0, sticky='NEW')

    def save_data(self, event):
        if self.n_s.get() and self.sn_s.get() and self.m_s.get():
            if self.n_s.get() != 'Insert name' and self.sn_s.get() != 'Insert surname' and self.m_s.get() != 'Insert membership':
                if self.m_s.get().isdigit():
                    name = self.n_s.get()
                    surn = self.sn_s.get()
                    mem = self.m_s.get()
                    client = client_dao.Client(id=self.id_now, name=name, surname=surn, mem=mem)
                    if self.id_now is None:
                        client_dao.DAO.insert(client.name, client.surname, client.mem)
                    else:
                        text = client_dao.DAO.update(client.id, client.name, client.surname, client.mem)
                        messagebox.showinfo(title='Actualizado', message=text)
                    self.reload_data()
                    self.clean_data(event=None)
                else:
                    messagebox.showerror(message='Error en la data ingresada, ingrese un numero de membresia')
                    self.m_s.set('')
                    self.m_s.focus_set()
            else:
                messagebox.showerror(message='Error en la data ingresada, complete todas las casillas')
                self.n_s.set('')
                self.n_s.focus_set()
        else:
            messagebox.showerror(message='Error en la data ingresada, complete todas las casillas')
            self.n_s.set('')
            self.n_s.focus_set()

    def delete_data(self, event):
        if self.select and self.id_now is not None:
            name = self.n_s.get()
            surn = self.sn_s.get()
            mem = self.m_s.get()
            client = client_dao.Client(id=self.id_now, name=name, surname=surn, mem=mem)
            text = client_dao.DAO.delete(client.id)
            self.reload_data()
            self.clean_data(event=None)
            messagebox.showerror(title='Eliminado', message=text)
        else:
            messagebox.showerror(message='Error, no ha seleccionado ningun cliente')

    def clean_data(self, event):
        self.n_s.set('Insert name')
        self.sn_s.set('Insert surname')
        self.m_s.set('Insert membership')
        self.id_now = None
        self.reload_data()

    def btts(self):
        btn_save = ttk.Button(self.f_buttons, text='Save')
        btn_delete = ttk.Button(self.f_buttons, text='Delete')
        btn_clean = ttk.Button(self.f_buttons, text='Clean')
        btn_save.grid(column=0, row=0)
        btn_delete.grid(column=1, row=0)
        btn_clean.grid(column=2, row=0)
        btn_save.bind('<Button-1>', self.save_data)  # cuando toco el boton
        btn_delete.bind('<Button-1>', self.delete_data)  # cuando toco el boton
        btn_clean.bind('<Button-1>', self.clean_data)  # cuando toco el boton


if __name__ == '__main__':
    win = App()
    win.mainloop()
