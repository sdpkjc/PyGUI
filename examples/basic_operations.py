from pygui import clipboard, display, keyboard, mouse, window


def main():
    print("PyGUI Basic Operations Example")
    print("=" * 50)

    print("\n1. Mouse Operations")
    pos = mouse.position()
    print(f"Current mouse position: {pos}")

    mouse.move(500, 300, duration=0.5)
    print("Moved mouse to (500, 300)")

    print("\n2. Keyboard Operations")
    keyboard.write("Hello, PyGUI!")
    print("Typed: Hello, PyGUI!")

    print("\n3. Display Information")
    displays = display.all()
    print(f"Number of displays: {len(displays)}")
    for i, d in enumerate(displays):
        print(f"  Display {i + 1}: {d.bounds.width}x{d.bounds.height} @{d.scale}x DPI")

    print("\n4. Window Management")
    windows = window.list()
    print(f"Number of visible windows: {len(windows)}")
    if windows:
        print(f"  Active window: {windows[0].title}")

    print("\n5. Clipboard Operations")
    clipboard.set_text("PyGUI test")
    text = clipboard.get_text()
    print(f"Clipboard text: {text}")

    print("\n" + "=" * 50)
    print("Example completed!")


if __name__ == "__main__":
    main()
