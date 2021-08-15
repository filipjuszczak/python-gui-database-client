"""
A simple GUI database client.
User can add new records, show those which already exist, update records
and delete them.
"""

import tkinter
from tkinter import messagebox
import sqlite3

root = tkinter.Tk()
root.geometry('400x400')
root.title('Databases')

first_name = tkinter.Entry(root, width=30)
first_name.grid(row=0, column=1, padx=20, pady=(10, 0))

last_name = tkinter.Entry(root, width=30)
last_name.grid(row=1, column=1)

address = tkinter.Entry(root, width=30)
address.grid(row=2, column=1)

city = tkinter.Entry(root, width=30)
city.grid(row=3, column=1)

state = tkinter.Entry(root, width=30)
state.grid(row=4, column=1)

zipcode = tkinter.Entry(root, width=30)
zipcode.grid(row=5, column=1)

record_id = tkinter.Entry(root, width=30)
record_id.grid(row=9, column=1, pady=(20, 0))

first_name_label = tkinter.Label(root, text='First name:')
first_name_label.grid(row=0, column=0, pady=(10, 0))

last_name_label = tkinter.Label(root, text='Last name:')
last_name_label.grid(row=1, column=0)

address_label = tkinter.Label(root, text='Address:')
address_label.grid(row=2, column=0)

city_label = tkinter.Label(root, text='City:')
city_label.grid(row=3, column=0)

state_label = tkinter.Label(root, text='State:')
state_label.grid(row=4, column=0)

zipcode_label = tkinter.Label(root, text='Zipcode:')
zipcode_label.grid(row=5, column=0)

id_label = tkinter.Label(root, text='ID:')
id_label.grid(row=9, column=0, pady=(20, 0))


def add_record():
    """
    Gets all input data and adds a record to the database.
    :return: None
    """
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()
    
    if cursor.execute('''
                    INSERT INTO addresses VALUES (
                        :first_name,
                        :last_name,
                        :address,
                        :city,
                        :state,
                        :zipcode
                        )        
                    ''',
                      {
                          'first_name': first_name.get(),
                          'last_name': last_name.get(),
                          'address': address.get(),
                          'city': city.get(),
                          'state': state.get(),
                          'zipcode': zipcode.get()
                      }):
        messagebox.showinfo('Information', 'Record added successfully!')
    else:
        messagebox.showerror('Error', 'There was an error when adding record.')
    
    connection.commit()
    connection.close()

    first_name.delete(0, tkinter.END)
    last_name.delete(0, tkinter.END)
    address.delete(0, tkinter.END)
    city.delete(0, tkinter.END)
    state.delete(0, tkinter.END)
    zipcode.delete(0, tkinter.END)


submit_button = tkinter.Button(root, text='Add record to database',
                               command=add_record)
submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=100)


def query():
    """
    Connects to database, fetches all records from a table and shows it on
    the window.
    :return: None
    """

    connection = sqlite3.connect('address_book.db')

    cursor = connection.cursor()
    cursor.execute('SELECT oid, * FROM addresses')

    records = cursor.fetchall()

    if len(records) == 0:
        results = 'There are 0 records in the database.'
    else:
        results = 'Existing records:\n\n'
        fields = (
            'ID',
            'First name',
            'Last name',
            'Address',
            'City',
            'State',
            'Zipcode'
        )
        
        for record in records:
            index = 0
            for data in record:
                results += '{0}: {1}\n'.format(fields[index], data)
                index += 1
            results += '\n'
    
    connection.commit()
    connection.close()
    
    records_window = tkinter.Toplevel()
    records_window.geometry('400x600')
    records_window.title('Records list')
    
    query_label = tkinter.Label(records_window, text=results,
                                anchor=tkinter.CENTER)
    query_label.pack()


query_button = tkinter.Button(root, text='Show records', command=query)
query_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=137)


def delete_record():
    """
    Connects to database and deletes a record.
    :return: None
    """

    connection = sqlite3.connect('address_book.db')

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM addresses WHERE oid = {0}'.format(
        record_id.get()))
    
    if type(cursor.fetchone()) == type(None):
        messagebox.showerror('Error', 'Record does not exist!')
        connection.close()
    else:
        answer = messagebox.askyesno('Are you sure?',
                                     'Are you sure you want to '
                                     'delete that record?')
        if answer:
            if cursor.execute(
                    'DELETE FROM addresses WHERE oid = {0}'.format(
                        record_id.get())):
                messagebox.showinfo('Information',
                                    'Record deleted successfully!')
            else:
                messagebox.showerror('Error', 'Record was not deleted.')
            connection.commit()
            connection.close()
        else:
            messagebox.showinfo('Information', 'Operation aborted.')


def update_record():
    """
    A new window with update form. Updates existing record in database.
    :return: None
    """

    connection = sqlite3.connect('address_book.db')

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM addresses WHERE oid = {0}'.format(
        record_id.get()))

    data = cursor.fetchone()
    
    if type(data) == type(None):
        messagebox.showerror('Error', 'Record does not exist!')
    else:
        update_window = tkinter.Toplevel()
        update_window.geometry('400x400')
        update_window.title('Update record')

        first_name_update = tkinter.Entry(update_window, width=30)
        first_name_update.grid(row=0, column=1, padx=20, pady=(10, 0))

        last_name_update = tkinter.Entry(update_window, width=30)
        last_name_update.grid(row=1, column=1)

        address_update = tkinter.Entry(update_window, width=30)
        address_update.grid(row=2, column=1)

        city_update = tkinter.Entry(update_window, width=30)
        city_update.grid(row=3, column=1)

        state_update = tkinter.Entry(update_window, width=30)
        state_update.grid(row=4, column=1)

        zipcode_update = tkinter.Entry(update_window, width=30)
        zipcode_update.grid(row=5, column=1)

        first_name_update_label = tkinter.Label(update_window,
                                                text='First name:')
        first_name_update_label.grid(row=0, column=0, pady=(10, 0))

        last_name_update_label = tkinter.Label(update_window,
                                               text='Last name:')
        last_name_update_label.grid(row=1, column=0)

        address_update_label = tkinter.Label(update_window, text='Address:')
        address_update_label.grid(row=2, column=0)

        city_update_label = tkinter.Label(update_window, text='City:')
        city_update_label.grid(row=3, column=0)

        state_update_label = tkinter.Label(update_window, text='State:')
        state_update_label.grid(row=4, column=0)

        zipcode_update_label = tkinter.Label(update_window, text='Zipcode:')
        zipcode_update_label.grid(row=5, column=0)

        first_name_update.insert(0, str(data[0]))
        last_name_update.insert(0, str(data[1]))
        address_update.insert(0, str(data[2]))
        city_update.insert(0, str(data[3]))
        state_update.insert(0, str(data[4]))
        zipcode_update.insert(0, str(data[5]))

        def update_selected_record():
            """
            Updates selected record.
            :return: None
            """
            response = messagebox.askyesno('Information', 'Are you sure '
                                                          'input data is '
                                                          'correct and you '
                                                          'want to update '
                                                          'that record?')
            if response:
                command = """
                UPDATE addresses SET first_name = '{0}',
                                     last_name = '{1}',
                                     address = '{2}',
                                     city = '{3}',
                                     state = '{4}',
                                     zipcode = '{5}'
                WHERE oid = {6}
                """.format(first_name_update.get(), last_name_update.get(),
                           address_update.get(), city_update.get(),
                           state_update.get(), zipcode_update.get(),
                           record_id.get())

                if cursor.execute(command):
                    messagebox.showinfo('Information', 'Record updated '
                                                       'successfully!')

                    connection.commit()
                    connection.close()
                    
                    update_window.destroy()
                else:
                    error_msg = 'There was an error during the record update'
                    messagebox.showerror('Error', error_msg)
                    
                    connection.close()
            else:
                messagebox.showinfo('Information', 'Operation aborted.')
                update_window.destroy()
                
                connection.close()

        update_button_update = tkinter.Button(update_window,
                                              text='Update record',
                                              command=update_selected_record)
        update_button_update.grid(row=6, column=0, columnspan=2, padx=10,
                                  pady=10, ipadx=137)


update_button = tkinter.Button(root, text='Update record',
                               command=update_record)
update_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=137)

delete_button = tkinter.Button(root, text='Delete record',
                               command=delete_record)
delete_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, ipadx=137)

root.mainloop()
