from collections import UserDict
from datetime import date, datetime,timedelta
from abc import ABC, abstractmethod


class UserInterface(ABC):

    @abstractmethod
    def show_message(self, message):
        pass

    @abstractmethod
    def show_records(self, records):
        pass

    @abstractmethod
    def show_help(self):
        pass

class ConsoleView(UserInterface):

    def show_records(self, records):

        for record in records:
            print(record)

    def show_message(self, message):
        print(message)


    def show_help(self):
        print("""
        Available commands:
  - hello
  - add [name] [phone]
  - change [name] [old phone] [new phone]
  - phone [name]
  - all
  - add-birthday [name] [DD.MM.YYYY]
  - show-birthday [name]
  - birthdays
  - close / exit
              """)


class Field:
    def __init__(self, value):
        if self.is_valid(value):
            self.value = value

    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def is_valid(self, value):
        if len(value) == 10 and value.isdigit():
            return True
        raise ValueError("Phone should be 10 digits long")



class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date().strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format.Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_number, new_number):
        phone_obj = self.find_phone(old_number)
        if phone_obj:
            self.add_phone(new_number)
            self.remove_phone(old_number)
        else:
            raise ValueError("Check length and correctness of the numbers")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record_object):
        self.data[record_object.name.value] = record_object

    def find(self, name):
        if name in self.data.keys():
            return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, days = 7):
        upcoming_birthdays = []
        today = datetime.today()

        for name, record in self.data.items():
            if not record.birthday or not record.birthday.value:
                continue
            birthday_in_date_format = datetime.strptime(record.birthday.value, "%d.%m.%Y")
            birthday_this_year = birthday_in_date_format.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_in_date_format.replace(year=today.year + 1)

            """
            Додайте на цьому місці перевірку, чи не буде 
            припадати день народження вже наступного року.
            """

            if 0 <= (birthday_this_year - today).days <= days:
                if birthday_this_year.weekday() >= 5:
                    days_ahead = 0 - birthday_this_year.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    birthday_this_year += timedelta(days=days_ahead)
                """ 
                Додайте перенесення дати привітання на наступний робочий день,
                якщо день народження припадає на вихідний. 
                """
                congratulation_date = birthday_this_year.strftime("%d.%m.%Y")
                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date})
        return upcoming_birthdays

    def __str__(self):
        result = ""
        for name, value in self.data.items():
            phones = ";".join(p.value for p in value.phones)
            result += f"Contact name : {name}, phones: {phones}\n"
        return result.strip()





