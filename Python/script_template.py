# import os

class Foo:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def main():
    foo = Foo('Matt', 38)
    someFunction(foo.name) 

def someFunction(name):
    print('Hello, ' + name)

if __name__ == "__main__":
    main()
