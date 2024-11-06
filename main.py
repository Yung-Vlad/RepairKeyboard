import keyboard as kb
import ctypes
import pystray
from pystray import MenuItem, Icon
from PIL import Image


def get_keyboard_layout() -> str:
    layout_id = ctypes.windll.user32.GetKeyboardLayout(0)
    layout_code = layout_id & 0xFFFF

    layouts = {
        0x0422: 'Ua',
        0x0409: 'En',
    }

    return layouts.get(layout_code, "Unknown layout!")


def remap_keys(e: kb.KeyboardEvent) -> bool:
    if not e.is_keypad:
        return True

    layout = get_keyboard_layout()  # Get layout (Eng or Ukr)

    if e.scan_code == 71 and e.event_type == "down": # 7 -> b
        kb.send(23 if layout == "Ua" else 48)
        return False
    elif e.scan_code == 72 and (e.name in ['8', "up"]) and e.event_type == "down": # 8 -> g
        kb.send(25 if layout == "Ua" else 34)
        return False

    return True


# Button exit in tray
def exit_action() -> None:
    global running
    running = False
    icon.stop()

def load_icon(path: str) -> Image:
    return Image.open(path)


if __name__ == "__main__":
    running = True  # Flag "Is running"

    kb.hook(remap_keys, suppress=True)

    # Icon for tray
    icon_path = "tray_icon.png"
    icon = Icon("RemapKeys")
    icon.icon = load_icon(icon_path)
    icon.title = "RemapKeys Application"
    icon.menu = pystray.Menu(
        MenuItem("Exit", exit_action)
    )

    icon.run()

    while running:
        kb.wait()

    kb.unhook_all()
