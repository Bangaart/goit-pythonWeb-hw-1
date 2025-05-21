import pickle
from classes import *

def input_error(func):  # Decorator for errors
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if not result:
                return "No contact was found with such name"
            return result
        except ValueError as e:
            if "not enough" in str(e):
                return "Enter all arguments for the command"
            else:
                return str(e)
        except IndexError as e:
            return str(e) if str(e) else "Enter user name"
        except KeyError as e:
            return str(e) if str(e) else "There is no such name"

    return inner


@input_error
def input_parcer(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_command(args: str, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact added"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args: str, book: AddressBook) -> str|None:
    name, old_phone, new_phone, *_ = args
    record: Record = book.find(name)
    message = "Phone changed"
    if record:
        record.edit_phone(old_phone, new_phone)
        return message


@input_error
def get_phone(args: str, book: AddressBook) -> str|None:
    name, *_ = args
    record: Record = book.find(name)
    if record:
        return f"{'; '.join(p.value for p in record.phones)}"

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_obj, *_ = args
    record : Record = book.find(name)
    message = "Birthday date added"
    if record:
        record.add_birthday(birthday_obj)
        return message

@input_error
def show_birthday(args: str, book: AddressBook):
    name , *_ = args
    record : Record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        return "There is no birthday date for the this contact"

@input_error
def birthdays(book: AddressBook) ->list[dict]|str:
    result = book.get_upcoming_birthdays()
    readable_format = ""
    for i in result:
        readable_format += f"{i["name"]}: congratulation_date - {i["congratulation_date"]}\n"
    return readable_format if readable_format else "No birthdays in next 7 days"


def get_all(book: AddressBook) -> str:
    result = ""
    if book:
        for key, record in book.items():
            phones = ",".join(p.value for p in record.phones)
            birthday_date = "Not specified yet" if record.birthday is None else record.birthday.value
            result += f"Contact name : {key}, phones: {phones}, birthday date: {birthday_date}\n"
        return result.strip()
    else:
        return "Address book is empty"

def save_data(book, filename="addressbook.pkl"):
    with open (filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename="addressbook.pkl"):
    with open(filename, "rb") as file:
        return pickle.load(file)

def main():
    view = ConsoleView()
    try:
        book = load_data()
    except FileNotFoundError:
        book = AddressBook()
    print("Welcome to assistant bot")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = input_parcer(user_input)

        if command in ["exit", "close"]:
            save_data(book)
            view.show_message("Good bye")
            break
        elif command == "hello":
            view.show_message("How can i help you")
        elif command == "add":
            view.show_message(add_command(args, book))
        elif command == "change":
            view.show_message(change_phone(args, book))
        elif command == "phone":
            view.show_message(get_phone(args, book))
        elif command == "all":
            a = [str(r) for r in book.values()]
            print(a)
        elif command == "add-birthday":
            view.show_message(add_birthday(args, book))
        elif command == "show-birthday":
            view.show_message(show_birthday(args, book))
        elif command == "birthdays":
            view.show_message(birthdays(book))
        elif command == "help":
            view.show_help()
        else:
            print("Invalid command or empty input")


if __name__ == "__main__":
    main()