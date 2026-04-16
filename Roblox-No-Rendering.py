import tkinter as tk
import win32gui
import win32con

TARGET_TITLE = "Roblox"


class WindowManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Window Manager (Optimized)")
        self.root.geometry("400x500")

        self.windows = {}  # hwnd -> UI frame
        self.cached_hwnds = set()

        self.auto_hide_new = tk.BooleanVar(value=False)
        self.auto_refresh = tk.BooleanVar(value=False)

        # ---------------- Top controls ----------------
        top = tk.Frame(root)
        top.pack(fill="x")

        tk.Checkbutton(
            top,
            text="Auto-hide new clients",
            variable=self.auto_hide_new
        ).pack(side="left")

        tk.Checkbutton(
            top,
            text="Auto-refresh",
            variable=self.auto_refresh
        ).pack(side="left")

        tk.Button(top, text="Refresh", command=self.refresh_windows).pack(side="right")
        tk.Button(top, text="Hide All", command=self.hide_all).pack(side="right")
        tk.Button(top, text="Show All", command=self.show_all).pack(side="right")

        # ---------------- List ----------------
        self.list_frame = tk.Frame(root)
        self.list_frame.pack(fill="both", expand=True)

        # Start lightweight loop (ONLY if auto-refresh is enabled)
        self.light_loop()

    # ---------------- Window scan ----------------

    def enum_windows(self):
        result = set()

        def callback(hwnd, _):
            if win32gui.IsWindow(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title == TARGET_TITLE:
                    result.add(hwnd)

        win32gui.EnumWindows(callback, None)
        return result

    # ---------------- Window actions ----------------

    def hide_window(self, hwnd):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        except:
            pass

    def show_window(self, hwnd):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        except:
            pass

    def toggle_window(self, hwnd):
        try:
            if win32gui.IsWindowVisible(hwnd):
                self.hide_window(hwnd)
            else:
                self.show_window(hwnd)
        except:
            pass

    def hide_all(self):
        for hwnd in list(self.windows.keys()):
            self.hide_window(hwnd)

    def show_all(self):
        for hwnd in list(self.windows.keys()):
            self.show_window(hwnd)

    # ---------------- UI handling ----------------

    def add_window(self, hwnd):
        frame = tk.Frame(self.list_frame, pady=2)
        frame.pack(fill="x")

        label = tk.Label(frame, text=f"Roblox HWND: {hwnd}")
        label.pack(side="left")

        btn = tk.Button(
            frame,
            text="Toggle",
            command=lambda h=hwnd: self.toggle_window(h)
        )
        btn.pack(side="right")

        self.windows[hwnd] = frame

        # auto-hide new clients
        if self.auto_hide_new.get():
            self.hide_window(hwnd)

    def remove_window(self, hwnd):
        frame = self.windows.pop(hwnd, None)
        if frame:
            frame.destroy()

    # ---------------- Core optimized refresh ----------------

    def refresh_windows(self):
        current_hwnds = self.enum_windows()

        # ONLY update differences (not full rebuild every time)
        new_hwnds = current_hwnds - self.cached_hwnds
        removed_hwnds = self.cached_hwnds - current_hwnds

        for hwnd in new_hwnds:
            self.add_window(hwnd)

        for hwnd in removed_hwnds:
            self.remove_window(hwnd)

        self.cached_hwnds = current_hwnds

    # ---------------- Lightweight loop ----------------

    def light_loop(self):
        # Only run auto-refresh if user enabled it
        if self.auto_refresh.get():
            self.refresh_windows()

        # MUCH slower loop = no lag
        self.root.after(3000, self.light_loop)  # every 3 seconds


if __name__ == "__main__":
    root = tk.Tk()
    app = WindowManagerApp(root)
    root.mainloop()
