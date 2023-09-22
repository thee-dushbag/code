class BigChain:
    def __init__(self, sep=None) -> None:
        self.steps = []
        self.sep = sep or " -> "

    @property
    def str_steps(self):
        result = self.sep.join(self.steps)
        self.steps.clear()
        return result

    def one(self):
        self.steps.append("one")
        print("Stepping: 'one'")
        return self

    def two(self):
        self.steps.append("two")
        print("Stepping: 'two'")
        return self

    def three(self):
        self.steps.append("three")
        print("Stepping: 'three'")
        return self

    def four(self):
        self.steps.append("four")
        print("Stepping: 'four'")
        return self

    def five(self):
        self.steps.append("five")
        print("Stepping: 'five'")
        return self

    def six(self):
        self.steps.append("six")
        print("Stepping: 'six'")
        return self

    def seven(self):
        self.steps.append("seven")
        print("Stepping: 'seven'")
        return self

    def eight(self):
        self.steps.append("eight")
        print("Stepping: 'eight'")
        return self

    def nine(self):
        self.steps.append("nine")
        print("Stepping: 'nine'")
        return self

    def ten(self):
        self.steps.append("ten")
        print("Stepping: 'ten'")
        return self
