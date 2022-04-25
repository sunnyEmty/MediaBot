class Print:
    def __int__(self):
        Print(self).print()

    def print(self):
        print('Принт')


class Cat(Print):
    def __int__(self):
        super().__int__()

    def print(self):
        super().print()
        print('Мяу')


Cat().print()