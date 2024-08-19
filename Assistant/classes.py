import re
from datetime import datetime, date, timedelta
from collections import UserDict
from abc import abstractmethod, ABC

class View(ABC):
    @abstractmethod
    def display(self, message):
        pass

    @abstractmethod
    def input(self, prompt):
        pass

class ConsoleView(View):
    def display(self, message):
        print(message)

    def input(self, prompt):
        return input(prompt)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(phone)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = self.validate_and_convert(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)
    def validate_and_convert(self, date_string):
        match = re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_string)
        if not match:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        try:
            date_object = datetime.strptime(date_string, "%d.%m.%Y").date()
            print (date_object, type(date_object))
            return date_object
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record():
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        self.phones = [phone for phone in self.phones if phone.value != number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def add_birthday(self, birthday_date):
        b = Birthday(birthday_date)
        self.birthday = b


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday date: {self.birthday}"

class AddressBook(UserDict):
    def __str__(self):
        contacts_str = ', '.join(f"{record}" for name, record in self.data.items())
        return f"Contacts: {contacts_str}"

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name_look_for):
        return self.data.get(name_look_for)

    def delete(self, name_to_delete):
        if name_to_delete in self.data:
            del self.data[name_to_delete]

    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    def date_to_string(self, date):
        return date.strftime("%Y.%m.%d")
    def get_upcaming_birthdays(self, book):
        upcoming_birthdays = []
        today = date.today()
        for rec in book.data:
            record = book.find(rec)
            birthday_this_year = record.birthday.value.replace(year=today.year)
            if 0 <= (birthday_this_year - today).days <= 7:
                birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                congratulation_date_str = self.date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays