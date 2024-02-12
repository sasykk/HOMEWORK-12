from types import FunctionType
from classes import AddressBook, Record
import pickle

class Bot:

    def __init__(self):
        self.book = AddressBook()
        self.file = "contacts.bin"
        try:
            with open(self.file, "rb") as f:
                contacts = pickle.load(f)
                self.book.data = contacts
        except:
            print("New book created")

    @staticmethod
    def input_error(func):
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except (KeyError, ValueError, IndexError) as e:
                return str(e)
        return inner

    @input_error
    def hello(self, _):
        return "How can I help you?"

    @input_error
    def add(self, customer_input):
        _, name, phone = customer_input.split()
        if name not in self.book.data.values():
            self.book.add_record(Record(name, phone))
            return self.book.data[name]
        raise TypeError("Contact already exists")

    @input_error
    def change(self, customer_input):
        _, name, old_phone, new_phone = customer_input.split()
        if name in self.book.data.keys():
            record = self.book.find(name)
            record.edit_phone(old_phone, new_phone)
            return record
        raise TypeError("Contact does not exists")

    @input_error
    def get_phone(self, customer_input):
        _, name = customer_input.split()
        try:
            result = self.book.data[name]
            return result
        except:
            raise TypeError("Contact not found")

    @input_error
    def show_all(self, customer_input):
        if customer_input != "show all":
            raise KeyError

        if len(self.book.data.values()) == 0:
            return "Contacts list is empty"
        
        sorted_records = sorted(self.book.data.items())
        records = "\n".join([str(i[1]) for i in sorted_records])

        return records

    @input_error
    def search(self, customer_input):
        _, text = customer_input.split()
        return self.book.search(text)

    @input_error
    def bye_bye(self, customer_input):
        if customer_input in ("good bye", "exit", "close"):
            with open(self.file, "wb") as f:
                pickle.dump(self.book.data, f)
            return "Good bye!"
        raise KeyError

    ACTIONS = {
        "hello": hello,
        "add": add,
        "change": change,
        "phone": get_phone,
        "show": show_all,
        "search": search,
        "exit": bye_bye,
        "close": bye_bye,
        "good": bye_bye
    }

    @input_error
    def get_action(self, customer_input):
        action = customer_input.split()[0]
        return self.ACTIONS[action]

    def main(self):
        while True:
            customer_input = input(">>> ").lower().strip()
            function = self.get_action(customer_input)
            if not isinstance(function, FunctionType):
                print(function)
                continue
            result = function(self, customer_input)
            print(result)

            if result == "Good bye!":
                break
