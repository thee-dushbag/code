"""
THE ADAPTER DESIGN PATTERN
==========================
The Adapter pattern allows incompatible
interfaces to work together. In this example,
the Target class defines the expected interface,
the Adaptee class has a different interface,
and the Adapter class bridges the gap.
The Adapter class wraps an instance of Adaptee
and implements the Target interface, translating
calls to match the Adaptee's interface.
The client code demonstrates how the Adapter
allows the client to use the Adaptee through
the Target interface."""


class Target:
    def request(self):
        pass


class Adaptee:
    def specific_request(self):
        return "Adaptee method called"


class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return self.adaptee.specific_request()


# Client code
adaptee = Adaptee()
adapter = Adapter(adaptee)

result = adapter.request()
print("Adapter request result:", result)
