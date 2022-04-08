from django.dispatch import Signal, receiver

update_s = Signal()

class Show:
    i = 0

    def print_i(self):
        while True:
            print(Show.i)

    @receiver(update_s)
    def update_i(self, **kwargs):
        i = kwargs['i']

def send_i(i):




