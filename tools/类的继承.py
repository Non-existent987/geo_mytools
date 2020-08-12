# coding=UTF-8
class SchoolMember:
    '''代表任何学校里的成员。 '''
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print('1--__init__---初始化1: {}-----'.format(self.name))
    def tell2(self):
        '''告诉我有关我的细节。 '''
        print('1tell-----名字:"{}" 年龄:"{}"'.format(self.name, self.age), end=" ")

class Teacher(SchoolMember):
    '''代表一位老师。 '''
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print('2--__init__---初始化2: {}-----'.format(self.name))
    def tell(self):
        SchoolMember.tell2(self)
        print('2tell-----Salary: "{:d}"'.format(self.salary))

class Student(SchoolMember):
    '''代表一位学生。 '''
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print('3--__init__---初始化3: {}-----'.format(self.name))
    def tell(self):
        SchoolMember.tell2(self)
        # print('3tell-----Marks: "{:d}"'.format(self.marks))

t = Teacher('李老师', 40, 30000)
s = Student('学生', 25, 75)
z = SchoolMember('\n主人', 28)
# 打印一行空白行
print()
members = [t, s ]
for member in members:
    # 对全体师生工作
    member.tell()
z.tell2()