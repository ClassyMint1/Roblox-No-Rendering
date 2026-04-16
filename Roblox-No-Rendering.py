import time
import win32gui
import win32con

seen_windows = set()
IGNORE_HWND = None  # put a hwnd here if you want to ignore a specific one

def window_callback(hwnd, _):
    global seen_windows

    title = win32gui.GetWindowText(hwnd)

    if title == "Roblox" and win32gui.IsWindowVisible(hwnd):

        # Ignore specific window if set
        if hwnd == IGNORE_HWND:
            return

        # If we've already seen this window, skip it
        if hwnd in seen_windows:
            return

        # Mark as seen (so existing ones won't be touched again)
        seen_windows.add(hwnd)

        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        win32gui.PostMessage(
            hwnd,
            win32con.WM_SYSCOMMAND,
            win32con.SC_MINIMIZE,
            0
        )
        print(f"Found NEW Roblox window {hwnd}")

print("Only NEW Roblox windows will be hidden.")

# First pass: collect already open windows so they are ignored
def init_callback(hwnd, _):
    title = win32gui.GetWindowText(hwnd)
    if title == "Roblox" and win32gui.IsWindowVisible(hwnd):
        seen_windows.add(hwnd)

win32gui.EnumWindows(init_callback, None)

# Main loop
while True:
    win32gui.EnumWindows(window_callback, None)
    time.sleep(0.001)