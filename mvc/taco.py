class Automobile(object):
    wheels = 4
    engine = True

    def __init__(self, man, model, color):
        self.manufacturer = man
        self.model = model
        self.color = color

    def go_forward(self):
        return "Move forward"

    def go_backward(self):
        return "Move backward"

    def __str__(self):
        return self.manufacturer


class Car(Automobile):

    def __init__(self):
        pass
