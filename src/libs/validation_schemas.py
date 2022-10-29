import datetime
from datetime import date
import re
from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'


    @abstractmethod
    def value(self):
        ...


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            value.isdigit()
        except Exception:
            print("Value Error, phone should contain numbers")
            raise ValueError


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return 'N/A'
        else:
            return f'{self.value:%d %b %Y}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                print("Enter the date of birth in the format dd.mm.yyyy")


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        result = None
        get_email = re.findall(r'\b[a-zA-Z]\w+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
        for i in get_email:
            result = i
        if result is None:
            raise AttributeError(f" Incorrect email {value}")
        self.__value = result


class DateIsNotValid(Exception):
    pass


class Decorator:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            print('Error! Give me name and phone or birthday please!')
        except KeyError:
            print('Error! User not found!')
        except ValueError:
            print('Error! Phone number is incorrect!')
        except DateIsNotValid:
            print('Error! Date is incorrect!')
