class Student:
    def __init__(self, student_id, name, age, gender, school, class_name, division, mobile, email, father_name, address):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.school = school
        self.class_name = class_name
        self.division = division
        self.mobile = mobile
        self.email = email
        self.father_name = father_name
        self.address = address

    def __str__(self):
        """String representation of a student object for debugging."""
        return f"ID: {self.student_id}, Name: {self.name}, Mobile: {self.mobile}"
