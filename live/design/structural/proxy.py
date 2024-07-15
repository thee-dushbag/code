"""
PROXY DESIGN PATTERN
====================
The Proxy pattern provides a surrogate or
placeholder for another object to control
access to it. In this example, the Subject
defines the interface for real subjects and
proxies. RealSubject implements the real
functionality. Proxy class maintains a reference
to the real subject and adds behavior to control
access. The client code demonstrates how the
proxy can intercept and control requests
to the real subject."""


class Subject[T]:
    def request(self) -> T:
        raise NotImplementedError


class RealSubject(Subject[str]):
    def request(self):
        return "RealSubject request"


class Proxy(Subject[str]):
    def __init__(self, real_subject: RealSubject):
        self.real_subject = real_subject

    def request(self):
        return f"Proxy request calling real subject: {self.real_subject.request()}"


# Client code
real_subject = RealSubject()
proxy = Proxy(real_subject)

result_real = real_subject.request()
result_proxy = proxy.request()

print("Real Subject result:", result_real)
print("Proxy result:", result_proxy)
