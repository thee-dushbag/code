# Abstract Factory
# Provides an interface for creating families of related
# or dependent objects without specifying their concrete classes.

from abc import ABC, abstractmethod
from typing import Callable, TypeVar

T = TypeVar("T", covariant=True)

EventCallback = Callable[[T], None]


# Abstract Component interfaces
class Event:
    ...


class ChangeEvent(Event):
    def __init__(self, oldvalue, newvalue) -> None:
        self.oldvalue = oldvalue
        self.newvalue = newvalue


class EventCallbacks:
    def __init__(self) -> None:
        self._callbacks: dict[str, EventCallback[Event]] = {}

    def _register(self, key: str, callback: EventCallback):
        self._callbacks[key] = callback

    def _get(self, key: str):
        return self._callbacks.get(key)

    def _fire(self, key: str, event: Event):
        if callback := self._get(key):
            callback(event)


class Component(ABC):
    @abstractmethod
    def display(self):
        pass

    def _opengl_render(self):
        print(f"Allocating buffers for : {self.__class__.__name__!r}")
        self.display()

    def render(self):
        self._opengl_render()


# Event Mixins
class OnClick(EventCallbacks):
    KEY = "onclick"

    def onclick(self, callback: EventCallback[Event]):
        self._register(self.KEY, callback)

    def click(self, event: Event):
        self._fire(self.KEY, event)


class OnChange(EventCallbacks):
    KEY = "onchange"

    def onchange(self, callback: EventCallback[ChangeEvent]):
        self._register(self.KEY, callback)

    def change(self, event: ChangeEvent):
        self._fire(self.KEY, event)


class Button(Component, OnClick):
    ...


class Checkbox(Component, OnClick):
    ...


class TextInput(Component, OnChange):
    ...


class Label(Component):
    ...


# Concrete Components
class WindowsButton(Button):
    def display(self):
        print("Windows-style Button")


class WindowsCheckbox(Checkbox):
    def display(self):
        print("Windows-style Checkbox")


class WindowsLabel(Label):
    def display(self):
        print("Windows-style Label")


class WindowsTextInput(TextInput):
    def display(self):
        print("Windows-style TextInput")


class MacButton(Button):
    def display(self):
        print("Mac-style Button")


class MacCheckbox(Checkbox):
    def display(self):
        print("Mac-style Checkbox")


class MacTextInput(TextInput):
    def display(self):
        print("Mac-style TextInput")


class MacLabel(Label):
    def display(self):
        print("Mac-style Label")


class WebButton(Button):
    def display(self):
        print("Web-style Button")


class WebCheckbox(Checkbox):
    def display(self):
        print("Web-style Checkbox")


class WebTextInput(TextInput):
    def display(self):
        print("Web-style TextInput")


class WebLabel(Label):
    def display(self):
        print("Web-style Label")


# Abstract Factory interface
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

    @abstractmethod
    def create_label(self) -> Label:
        pass

    @abstractmethod
    def create_textinput(self) -> TextInput:
        pass


# Concrete Factories
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

    def create_label(self) -> Label:
        return WindowsLabel()

    def create_textinput(self) -> TextInput:
        return WindowsTextInput()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

    def create_label(self) -> Label:
        return MacLabel()

    def create_textinput(self) -> TextInput:
        return MacTextInput()


class WebFactory(GUIFactory):
    def create_button(self) -> Button:
        return WebButton()

    def create_checkbox(self) -> Checkbox:
        return WebCheckbox()

    def create_label(self) -> Label:
        return WebLabel()

    def create_textinput(self) -> TextInput:
        return WebTextInput()


# Abctract Window Factory
class Window(ABC):
    def __init__(self, factory: GUIFactory) -> None:
        self.factory = factory
        self.components = []

    @abstractmethod
    def build(self):
        pass

    def place(self, *components: Component):
        self.components.extend(components)

    def show(self):
        self.build()
        self._show()

    def _show(self):
        for component in self.components:
            component.render()


class _BuildMixinWindow(Window):
    def _build(self):
        button = self.factory.create_button()
        button.onclick(lambda e: print("Button Clicked..."))
        button.click(Event())
        checkbox = self.factory.create_checkbox()
        label = self.factory.create_label()
        textinput = self.factory.create_textinput()
        textinput.onchange(
            lambda e: print(f"Changed from {e.oldvalue!r} to {e.newvalue!r}")
        )
        textinput.change(ChangeEvent("simon", "nganga"))
        self.place(button, checkbox, label, textinput)


class WindowsWindow(_BuildMixinWindow):
    def __init__(self) -> None:
        super().__init__(WindowsFactory())

    def build(self):
        print("Windows-style Window")
        self._build()


class MacWindow(_BuildMixinWindow):
    def __init__(self) -> None:
        super().__init__(MacFactory())

    def build(self):
        print("Mac-style Window")
        self._build()


class WebWindow(_BuildMixinWindow):
    def __init__(self) -> None:
        super().__init__(WebFactory())

    def build(self):
        print("Web-style Window")
        self._build()


def opengl_hook(window: Window):
    print("Hooking to OpenGL Interfaces...")
    window.show()
    print("Unhooking and releasing resources...")


if __name__ == "__main__":
    # window = WindowsWindow() # Create Windows-style GUI components
    # window = MacWindow()     # Create Mac-style GUI components
    window = WebWindow()  # Create Web-style GUI components
    opengl_hook(window)
