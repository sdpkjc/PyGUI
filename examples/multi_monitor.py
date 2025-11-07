import time

from guiguigui import display, mouse


def main():
    print("GuiGuiGui Multi-Monitor Example")
    print("=" * 50)

    displays = display.all()
    print(f"\nDetected {len(displays)} display(s):")

    for i, d in enumerate(displays):
        print(f"\nDisplay {i + 1}:")
        print(f"  Name: {d.name}")
        print(f"  Resolution: {d.bounds.width}x{d.bounds.height}")
        print(f"  Position: ({d.bounds.x}, {d.bounds.y})")
        print(f"  Scale: {d.scale}x")
        print(f"  Primary: {d.is_primary}")

    print("\n" + "=" * 50)
    print("Moving mouse to center of each display...")

    for i, d in enumerate(displays):
        center = d.bounds.center
        print(f"\nMoving to Display {i + 1} center: ({center.x}, {center.y})")
        mouse.smooth_move(center.x, center.y, duration=0.5)
        time.sleep(0.5)

    print("\nCompleted!")


if __name__ == "__main__":
    main()
