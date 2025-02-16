# SCOPES
# Global scope
x = 10


def outer_function():
    # Enclosing scope
    y = 20
    x = 100  # Local to outer_function

    def inner_function():
        # Local scope
        z = 30
        try:
            print("Inner function:")
            print("x =", x)  # Local to outer_function
            print("y =", y)  # Enclosing variable
            print("z =", z)  # Local variable
            # Error: a not defined
            # print("a =", a)
        except Exception as e:
            print("Error in inner_function:", e)

    try:
        inner_function()
        print("Outer function:")
        print("x =", x)  # Local to outer_function
        print("y =", y)  # Enclosing variable
        # Error: z not in this scope
        # print("z =", z)
    except Exception as e:
        print("Error in outer_function:", e)

    print(x)  # Local to outer_function


for i in range(10):
    print(i)  # Loop variable
    print("hello")

try:
    outer_function()
    print("Global scope:")
    print("x =", x)  # Global variable
    # Error: y not in this scope
    print("y =", y)
    # Error: z not in this scope
    # print("z =", z)
except Exception as e:
    print("Error in global scope:", e)


# Instance scope
class MyClass:
    a = 40  # Class variable
    MY_CLASS_CONSTANT = 100  # Class constant

    def __init__(self, b):
        self.b = b  # Instance attribute

    def instance_method(self):
        y = 20  # Method variable
        try:
            print("Class method:")
            print("x =", x)  # Global variable
            print("y =", y)  # Method variable
            print("a =", MyClass.a)  # Class variable
            print("b =", self.b)  # Instance variable
            # Error: a not defined
            # print("a =", a)
        except Exception as e:
            print("Error in class_method:", e)


# Create an instance of MyClass with an instance attribute
# and call the class method
my_instance = MyClass(50)
my_another_instance = my_instance
my_instance.instance_method()
MyClass.a = 99  # Modify class variable
my_instance.instance_method()

# MUTABLE VARIABLES
# Example of mutable change in a list
my_list = [1, 2, 3]
# Create a second reference to the same list
another_list_reference = my_list
my_int = 90
my_another_integer = my_int
my_another_integer = 100  # This does not affect my_int


def modify_list(lst):
    lst.append(4)  # Modify the list
    print("Inside function:", lst)


print("Before function call:", my_list)
modify_list(my_list)
another_list_reference.append(109)  # Modify the list using another reference
print("After function call:", my_list)
print("After function call:", another_list_reference)


# Modify the list using the second reference
def modify_list_again(lst):
    lst.append(5)  # Modify the list
    print("Inside second function:", lst)


print("Before second function call:", another_list_reference)
modify_list_again(another_list_reference)
print("After second function call:", another_list_reference)
print("Original list after second function call:", my_list)
