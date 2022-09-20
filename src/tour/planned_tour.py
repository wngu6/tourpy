from generator import Generator


class PlannedTour(Generator):
    index: str = 1

    def __init__(self, basis_set, cycle: bool = True):
        self.basis_set = basis_set
        self.cycle = cycle

    def generate(self, current, data):
        if self.cycle:
            current = self.index
            self.index = self.index % self.basis_set.shape[0] + 1
            return self.basis_set[current - 1]
        else:
            self.index += 1
            if self.index > self.basis_set.shape[1]:
                return None
