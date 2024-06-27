import torch


class Person:
    def __init__(self, name, yob):
        self.name = name
        self.yob = yob

    def describe(self):
        """super method"""
        pass


class Student(Person):
    def __init__(self, name, yob, grade):
        super(Student, self).__init__(name, yob)
        self.grade = grade

    def describe(self):
        print(
            f'Student - Name: {self.name} - YoB: {self.yob} - Grade: {self.grade}')


class Teacher(Person):
    def __init__(self, name, yob, subject):
        super(Teacher, self).__init__(name, yob)
        self.subject = subject

    def describe(self):
        print(
            f'Teacher - Name: f{self.name} - YoB: {self.yob} - Subject: {self.subject}')


class Doctor(Person):
    def __init__(self, name, yob, specialist):
        super(Doctor, self).__init__(name, yob)
        self.specialist = specialist

    def describe(self):
        print(
            f'Doctor - Name : f{self.name} - YoB : {self.yob} - Grade : {self.specialist}')


class Ward:
    def __init__(self, name):
        self.name = name
        self.people = []

    def add_person(self, person: Person):
        self.people.append(person)

    def describe(self):
        print(f'Ward Name : {self.name}')
        for person in self.people:
            person.describe()

    def compute_average(self):
        yob = torch.tensor(
            [person.yob for person in self.people]).type(torch.float16)
        return yob.mean().item()

    def sort_age(self):
        yob = torch.tensor([person.yob for person in self.people])
        _, indides = torch.sort(yob, descending=True)
        people = []
        for i in indides:
            people.append(self.people[i])
        self.people = people

    def count_doctor(self):
        count = 0
        for person in self.people:
            if isinstance(person, Doctor):
                count += 1
        return count
