from collections import UserDict
from datetime import date, datetime

class Field:

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if self.is_valid(val):
            self.__value = val
        else:
            raise ValueError

    def is_valid(self, _):
        return True

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):

    def is_valid(self, value):
        if value.isdigit() and len(value) == 10:
            return True
        else:
            return False

class Birthday(Field):

    def is_valid(self, value):
        if bool(datetime.strptime(value, "%d.%m.%Y")):
            return True
        else:
            return False

class Record:

    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        if phones:
            self.phones.append(Phone(phones))
        self.birthday = Birthday(birthday).value if birthday else " "

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone):
        for idx, ph in enumerate(self.phones):
            if ph.value == phone:
                self.phones.pop(idx)

    def edit_phone(self, phone, new_phone):
        for idx, ph in enumerate(self.phones):
            if ph.value == phone:
                if ph.is_valid(new_phone):
                    self.phones[idx].value = new_phone
                    break
        else:
            raise ValueError("Phone not found")

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph

    def days_to_birthday(self):
        delta_days = None

        if self.birthday:
            day, month, _ = [int(i) for i in self.birthday.split('.')]

            current_date = date.today()
            current_year_birthday = datetime(
                current_date.year,
                month,
                day
            ).date()

            delta_days = int(str((current_year_birthday - current_date).days))

            if current_year_birthday < current_date:
                next_year_birthday = datetime(
                    current_date.year + 1,
                    month,
                    day
                ).date()

                delta_days = int(str((next_year_birthday - current_date).days))

        return delta_days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        record = None if name not in self.data else self.data[name]
        return record

    def delete(self, name):
        self.data.pop(name, None)

    def search(self, text):
        normalized_text = text.strip()
        result = []
        for record in self.data.values():
            phone = ' '.join(p.value for p in record.phones)
            if normalized_text in record.name.value.lower() or normalized_text in phone or normalized_text in record.birthday:
                result.append(str(record))
        return "\n".join(result)

    def iterator(self, records_num):
        list_book_values = list(self.data.values())
        counter = 0
        records = records_num if len(list_book_values) >= records_num else len(list_book_values)
        updated_records = records

        while counter < len(list_book_values):
            yield [str(record) for record in list_book_values[counter:updated_records]]
            counter += records
            updated_records += records

    def __str__(self):
        return "\n".join([str(r) for r in self.data.values()])
