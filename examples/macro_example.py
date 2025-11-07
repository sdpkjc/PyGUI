from pygui import Macro
from pygui.core.macro import KeyHotkey, KeyWrite, MouseClick, MouseMove


def simple_macro():
    login = (
        Macro("auto_login")
        .add(MouseMove(300, 200, 0.2))
        .add(MouseClick())
        .add(KeyWrite("username"))
        .wait(0.1)
        .add(MouseMove(300, 250, 0.2))
        .add(MouseClick())
        .add(KeyWrite("password"))
        .add(KeyHotkey(("enter",)))
    )

    print("Running login macro...")
    login.run()
    print("Macro completed!")


def copy_paste_macro():
    copy_paste = (
        Macro("copy_paste")
        .add(KeyHotkey(("cmd", "a")))
        .wait(0.1)
        .add(KeyHotkey(("cmd", "c")))
        .wait(0.1)
        .add(KeyHotkey(("cmd", "v")))
    )

    print("Running copy-paste macro...")
    copy_paste.run()
    print("Macro completed!")


if __name__ == "__main__":
    print("PyGUI Macro Examples")
    print("=" * 50)

    print("\n1. Simple Login Macro")
    simple_macro()

    print("\n2. Copy-Paste Macro")
    copy_paste_macro()

    print("\n" + "=" * 50)
