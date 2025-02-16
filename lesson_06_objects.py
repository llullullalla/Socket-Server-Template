# basics of objects and classes


class Car:
    def __init__(self, fuel_consuption, color):
        # 'self' is a special keyword that allows to access the
        # reference to the 'instance' of the class. All instance
        # methods should have 'self' as the first argument.
        self.fuel_consuption = fuel_consuption
        self.color = color
        # ENCAPSULATION (Internal state can not be changed by the user)
        # It is also sometimes called 'data hiding'.
        # In python it is achieved by putting and underscore as a
        # prefix to the attribute name.
        self._fuel_amount = 100

    def get_fuel(self):
        # it is a common pattern to give a copy
        # of an internal state to the user by a 'getter' method.
        return self._fuel_amount

    def refuel(self, fuel):
        # ABSTRACTION (The complex functionality implementation is hidden)
        # This allows users of your class to focus on higher level
        # functionality by hiding unnecessary details
        self._fuel_amount = fuel * 0.6 - 7 + 5

    def drive(self):
        self._fuel_amount -= self.fuel_consuption
        if self._fuel_amount <= 0:
            print("oh no! I am out of fuel")


# some examples with our new class 'Car'
my_pretty_car = Car(7, "pink")  # instantiation of the class
my_pretty_car.drive()  # method call
print(my_pretty_car.get_fuel())
my_pretty_car.refuel(70)
print("---")


# INHERITANCE (We can use a parent class for other classes)
# By inheritign from the parent class we inherit all the attributes
# and methods. The class can be further extended with
# additional behavior as well as it possible to override the behavior
# of the parent class.
class Porsche(Car):
    def drive(self):
        # POLYMORPHISM (Same method name, different behavior)
        # Polymorphism has many shapes (haha) in programming.
        # Later on we can call the method 'drive' as if it was
        # the parent method although the bavior will be different.
        print("I am Porsche and driving super fast!")
        # calling super() will give you a reference to the parent class.
        super().drive()

    def open_door(self):
        # this method is an entirely unique for 'Porsche'. The parent
        # class 'Car' does not have it.
        print("Door opened")


class Toyota(Car):
    def __init__(self, fuel_consuption, color):
        super().__init__(fuel_consuption, color)
        print(f"I am {self.color}!")

    def refuel(self, fuel):
        # This will 'override' the implementation of the parent class method.
        print("Toytas can not refuel!")

    def drive(self):
        # This will extend the implementation of the parent class method.
        # (Because we call the super method drive on the parent class as well)
        print("I am Toyota and driving very slow :(")
        super().drive()


car_array = [Car(10, "black"), Porsche(30, "gray"), Toyota(5, "blue")]
# POLYMORPHISM (Same method name, different behavior)
# we can iterate over the list and call the 'drive' method
# as if it was the same object class.
print("---")
for i in range(5):
    for car in car_array:
        car.drive()
