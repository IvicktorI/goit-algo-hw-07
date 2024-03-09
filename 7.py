from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value : str):
           super().__init__(value)
           
    def __eq__(self, other):
        return isinstance(other, Name) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

class Phone(Field):
    def __init__(self, value: str):
        if self.is_valid_number(value):
            super().__init__(value)
        else:
            raise ValueError("Incorrect phone number")
    @staticmethod
    def is_valid_number(number: str):
        return str(number).isdigit() and len(str(number)) == 10
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value=dtdt.strptime(value, "%Y.%m.%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: str,phone=None):
        self.name = Name(name)
        if phone==None:
            self.phones = []
        else:
            _phone=Phone(phone)
            self.phones = [_phone]
        self.birthday=None
    
    def add_phone(self,phone: str):
        flag=1
        for ph in self.phones:
            if ph.value==phone:
                flag=0
                break
        if flag:
            self.phones.append(Phone(phone))
        
    def remove_phone(self, phone: str):
        for ph in self.phones:
            if ph.value==phone:
                self.phones.remove(ph)
                break
    
    def edit_phone(self,old_phone: str, new_phone: str):
        for ph in self.phones:
            if ph.value==old_phone:
                ph.value = new_phone
                return 1
        return 0
        
    def find_phone(self, phone: str) ->Phone:
        for ph in self.phones:
            if ph.value==phone:
                return ph
    
    def add_birthday(self,birthday: str):
        self.birthday=Birthday(birthday)
            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday.value}"
    
class AddressBook(UserDict):      
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self,name: str):
        return self.data.get(name,None)
         

    def delete(self,name):
        del self.data[name]
    
    def edit_record(self,name,old_phone,new_phone) -> str:
        for contact in self.data:
            if contact==name:
                contact.edit_phone(Phone(old_phone),Phone(new_phone)) 
                return 'Record change'
        return 'Record not found'  
                
    def show_all(self):
        for contact in self.data.values():
            print(contact)

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'{e}'
        except KeyError:
            return 'No such name found'
        except IndexError:
            return 'Not found'
        except Exception as e:
            return f'Error: {e}'

    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_record(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def edit_phone(args, contacts):
    if len(args)==3:
        name, old_phone, new_phone = args
    else :
        raise ValueError ('Insufficient parameters')
    if name in contacts:
        if contacts[name].edit_phone(old_phone,new_phone):
            return "Record change."
    return 'Record not found'

@input_error
def add_phone(args, contacts):
    if len(args)==2:
        name, phone = args
    else :
        raise ValueError ('Insufficient parameters')
    if name in contacts:
        contacts[name].add_phone(phone)
        return "Phone add."
    else:
        return 'Record not found'

@input_error
def delete_phone(args, contacts):
    if len(args)==2:
        name, phone = args
    else :
        raise ValueError ('Insufficient parameters')
    if name in contacts:
        contacts[name].remove_phone(phone)
        return "Phone delete."
    else:
        return 'Record not found'

@input_error
def find_record(args, contacts: AddressBook):
    name = args[0]
    rec=contacts.find(name)
    if rec is not None:
        return rec
    else : 
        return 'Record not found'
   
@input_error 
def delete_record(args, contacts: AddressBook):
    name = args[0]
    contacts.delete(name)
    return f'Record delete'

@input_error
def show_all(contacts: AddressBook):
    contacts.show_all()
    
@input_error
def add_birthday(args, book):
    pass

@input_error
def show_birthday(args, book):
    pass

@input_error
def birthdays(args, book):
    pass


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case 'hello':
                print('How can I help you?')
            case 'add':
                print(add_record(args,book))
            case 'change':
                print(edit_phone(args,book))
            case 'phone':
                print(find_record(args,book))
            case 'delete':
                print(delete_record(args,book))
            case 'delete_phone':
                print(delete_phone(args, book))
            case 'all':
                print(show_all(book))
            case 'close':
                print('Good bye!')
                break
            case 'exit':
                print('Good bye!')
                break
            case _:
                print('Invalid command.')


if __name__ == "__main__":
    main()