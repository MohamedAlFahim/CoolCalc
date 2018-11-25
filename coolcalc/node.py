class Node:
    def __init__(self):
        raise NotImplementedError()

    def handle_signal(self, signal):
        raise NotImplementedError()

    @property
    def latex(self, *args):
        raise NotImplementedError()
