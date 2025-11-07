import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .types import Key


class MacroContext:
    def __init__(self, macro: "Macro"):
        self.macro = macro
        self.variables: dict[str, Any] = {}
        self.should_stop = False

    def set(self, name: str, value: Any) -> None:
        self.variables[name] = value

    def get(self, name: str, default: Any = None) -> Any:
        return self.variables.get(name, default)

    def stop(self) -> None:
        self.should_stop = True


class Action(ABC):
    @abstractmethod
    def execute(self, ctx: MacroContext) -> None:
        pass


@dataclass
class MouseMove(Action):
    x: int
    y: int
    duration: float = 0.0

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse

        mouse.move(self.x, self.y, self.duration)


@dataclass
class MouseClick(Action):
    button: str = "left"
    clicks: int = 1
    interval: float = 0.1

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse

        mouse.click(button=self.button, clicks=self.clicks, interval=self.interval)


@dataclass
class MouseDrag(Action):
    x: int
    y: int
    button: str = "left"
    duration: float = 0.0

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse

        mouse.drag(self.x, self.y, button=self.button, duration=self.duration)


@dataclass
class MouseScroll(Action):
    dx: int = 0
    dy: int = 0

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse

        mouse.scroll(self.dx, self.dy)


@dataclass
class KeyPress(Action):
    key: Key | str

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard

        keyboard.press(self.key)


@dataclass
class KeyRelease(Action):
    key: Key | str

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard

        keyboard.release(self.key)


@dataclass
class KeyTap(Action):
    key: Key | str
    times: int = 1
    interval: float = 0.05

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard

        keyboard.tap(self.key, self.times, self.interval)


@dataclass
class KeyWrite(Action):
    text: str
    interval: float = 0.0

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard

        keyboard.write(self.text, self.interval)


@dataclass
class KeyHotkey(Action):
    keys: tuple[Key | str, ...]

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard

        keyboard.hotkey(*self.keys)


@dataclass
class Wait(Action):
    seconds: float

    def execute(self, ctx: MacroContext) -> None:
        time.sleep(self.seconds)


@dataclass
class Repeat(Action):
    actions: list[Action]
    times: int

    def execute(self, ctx: MacroContext) -> None:
        for _ in range(self.times):
            if ctx.should_stop:
                break
            for action in self.actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break


@dataclass
class Condition(Action):
    condition: Callable[[MacroContext], bool]
    then_actions: list[Action]
    else_actions: list[Action] | None = None

    def execute(self, ctx: MacroContext) -> None:
        if self.condition(ctx):
            for action in self.then_actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break
        elif self.else_actions:
            for action in self.else_actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break


@dataclass
class Loop(Action):
    actions: list[Action]
    condition: Callable[[MacroContext], bool] | None = None
    max_iterations: int | None = None

    def execute(self, ctx: MacroContext) -> None:
        iterations = 0
        while True:
            if ctx.should_stop:
                break
            if self.condition and not self.condition(ctx):
                break
            if self.max_iterations and iterations >= self.max_iterations:
                break

            for action in self.actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break

            iterations += 1


class Macro:
    def __init__(self, name: str | None = None):
        self.name = name or "unnamed"
        self.actions: list[Action] = []

    def add(self, action: Action) -> "Macro":
        self.actions.append(action)
        return self

    def wait(self, seconds: float) -> "Macro":
        return self.add(Wait(seconds))

    def run(self, **variables) -> None:
        ctx = MacroContext(self)
        ctx.variables.update(variables)

        for action in self.actions:
            if ctx.should_stop:
                break
            action.execute(ctx)

    def repeat(self, times: int) -> None:
        for _ in range(times):
            self.run()


def macro(name: str | None = None) -> Macro:
    return Macro(name)
