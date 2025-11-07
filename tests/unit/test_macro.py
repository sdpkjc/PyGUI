from __future__ import annotations

import time

from guiguigui.core.macro import (
    Action,
    Condition,
    KeyPress,
    Loop,
    Macro,
    MacroContext,
    MouseClick,
    MouseMove,
    Repeat,
    Wait,
)
from guiguigui.core.types import Key


class CustomAction(Action):
    def __init__(self, func):
        self.func = func

    def execute(self, ctx: MacroContext) -> None:
        self.func()


class TestMacroActions:
    def test_wait_action(self) -> None:
        macro = Macro()
        wait = Wait(0.1)
        ctx = MacroContext(macro)
        start = time.time()
        wait.execute(ctx)
        elapsed = time.time() - start
        assert elapsed >= 0.1

    def test_mouse_move_action(self) -> None:
        macro = Macro()
        move = MouseMove(100, 200)
        ctx = MacroContext(macro)
        move.execute(ctx)

    def test_mouse_click_action(self) -> None:
        macro = Macro()
        click = MouseClick(button="left")
        ctx = MacroContext(macro)
        click.execute(ctx)

    def test_key_press_action(self) -> None:
        macro = Macro()
        press = KeyPress(Key.A)
        ctx = MacroContext(macro)
        press.execute(ctx)

    def test_repeat_action(self) -> None:
        counter = {"count": 0}

        def increment() -> None:
            counter["count"] += 1

        macro = Macro()
        repeat = Repeat([CustomAction(increment)], times=5)
        ctx = MacroContext(macro)
        repeat.execute(ctx)
        assert counter["count"] == 5

    def test_condition_action_true(self) -> None:
        executed = {"value": False}

        def set_true() -> None:
            executed["value"] = True

        macro = Macro()
        condition = Condition(lambda ctx: True, [CustomAction(set_true)])
        ctx = MacroContext(macro)
        condition.execute(ctx)
        assert executed["value"]

    def test_condition_action_false(self) -> None:
        executed = {"value": False}

        def set_true() -> None:
            executed["value"] = True

        macro = Macro()
        condition = Condition(lambda ctx: False, [CustomAction(set_true)])
        ctx = MacroContext(macro)
        condition.execute(ctx)
        assert not executed["value"]

    def test_loop_action(self) -> None:
        counter = {"count": 0}

        def increment() -> None:
            counter["count"] += 1

        def check_condition(ctx: MacroContext) -> bool:
            return counter["count"] < 3

        macro = Macro()
        loop = Loop([CustomAction(increment)], condition=check_condition)
        ctx = MacroContext(macro)
        loop.execute(ctx)
        assert counter["count"] == 3

    def test_custom_action(self) -> None:
        executed = {"value": False}

        def custom_func() -> None:
            executed["value"] = True

        macro = Macro()
        custom = CustomAction(custom_func)
        ctx = MacroContext(macro)
        custom.execute(ctx)
        assert executed["value"]


class TestMacro:
    def test_macro_builder(self) -> None:
        macro = Macro()
        macro.add(Wait(0.1))
        macro.wait(0.05)
        assert len(macro.actions) == 2

    def test_macro_run(self) -> None:
        counter = {"count": 0}

        def increment() -> None:
            counter["count"] += 1

        macro = Macro()
        macro.add(CustomAction(increment))
        macro.add(CustomAction(increment))
        macro.run()
        assert counter["count"] == 2

    def test_macro_with_context(self) -> None:
        macro = Macro()
        ctx = MacroContext(macro)
        ctx.set("test", "value")
        assert ctx.get("test") == "value"

    def test_macro_repeat_method(self) -> None:
        counter = {"count": 0}

        def increment() -> None:
            counter["count"] += 1

        macro = Macro()
        macro.add(CustomAction(increment))
        macro.repeat(times=3)
        assert counter["count"] == 3

    def test_macro_chain(self) -> None:
        result: list[str] = []

        macro = (
            Macro()
            .add(CustomAction(lambda: result.append("a")))
            .add(CustomAction(lambda: result.append("b")))
            .add(CustomAction(lambda: result.append("c")))
        )
        macro.run()
        assert result == ["a", "b", "c"]

    def test_macro_context_variables(self) -> None:
        macro = Macro()
        ctx = MacroContext(macro)
        ctx.set("x", 10)
        ctx.set("y", 20)
        assert ctx.get("x") == 10
        assert ctx.get("y") == 20
        ctx.set("z", 30)
        assert ctx.get("z") == 30

    def test_macro_context_stop(self) -> None:
        macro = Macro()
        ctx = MacroContext(macro)
        assert not ctx.should_stop
        ctx.stop()
        assert ctx.should_stop
