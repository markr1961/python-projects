#!/usr/bin/env python
# adapted from https://www.geeksforgeeks.org/create-a-pomodoro-using-python-tkinter/

"""Pomodoro Timer (Tkinter) — refactored to use subframes.

Changes vs. original:
- Uses three subframes (header/content/footer) for a clean layout.
- Replaces blocking while+sleep loops with Tkinter's `after()` so the UI stays responsive.
- Removes the global `pomo` reference; everything is instance-based.
- Keeps a persistent reference to the background image to prevent garbage collection.

Assets expected in the same folder:
- pomodoro.jpg
- sound.ogg
"""

import tkinter as tk        # https://tkdocs.com/
from tkinter import messagebox

from PIL import Image, ImageTk
from playsound import playsound
import time

# --- Settings ---
WORK_MIN = 38
SHORT_BREAK_MIN = 7

class Pomodoro:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("450x455")
        self.root.resizable(False, False)

        # State
        self._after_id = None
        self._mode = "work"  # 'work' or 'break'

        # --- Subframes ---
        # 1) Header: time display
        self.header = tk.Frame(self.root)
        self.header.pack(side=tk.TOP, fill=tk.X, padx=40, pady=(12, 6))

        # 2) Content: image/canvas
        self.content = tk.Frame(self.root)
        self.content.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=6)

        # 3) Footer: buttons
        self.footer = tk.Frame(self.root)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=(6, 12))

        self._build_header()
        self._build_content()
        self._build_footer()

        self._set_time(WORK_MIN * 60)

    # --------------------------- UI construction ---------------------------
    def _build_header(self):
        self.header.columnconfigure(0, weight=1)

        self.min_var = tk.StringVar(value=f"{WORK_MIN:02d}")
        self.sec_var = tk.StringVar(value="00")

        center_frame = tk.Frame(self.header)
        center_frame.grid(row=0, column=0)   # ✅ perfectly centered

        self.min_label = tk.Label(center_frame, textvariable=self.min_var,
                                  font=("arial", 22, "bold"),
                                  bg="red", fg="black", width=3)
        self.min_label.pack(side=tk.LEFT)

        tk.Label(center_frame, text=":", font=("arial", 22, "bold")).pack(side=tk.LEFT, padx=4)

        self.sec_label = tk.Label(center_frame, textvariable=self.sec_var,
                                  font=("arial", 22, "bold"),
                                  bg="black", fg="white", width=3)
        self.sec_label.pack(side=tk.LEFT)

        self.mode_label = tk.Label(center_frame, text="Work",
                                   font=("arial", 12, "bold"))
        self.mode_label.pack(side=tk.LEFT, padx=12)

    def _build_content(self):
        self.canvas = tk.Canvas(self.content, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and render background image (keep a reference!)
        img = Image.open("pomodoro.jpg")
        self.bg = ImageTk.PhotoImage(img)

        # Center the image inside the canvas
        self.canvas.bind("<Configure>", self._redraw_background)

    def _redraw_background(self, event=None):
        self.canvas.delete("bg")
        # place image near the top-left like the original, but relative to canvas
        self.canvas.create_image(90, 10, image=self.bg, anchor="nw", tags="bg")

    def _build_footer(self):
        # Use grid inside footer frame for nicer button alignment
        self.footer.columnconfigure((0, 1, 2), weight=1)

        self.btn_start = tk.Button(
            self.footer,
            text="Start Work",
            bd=5,
            command=self.start_work,
            bg="red",
            font=("arial", 13, "bold"),
        )
        self.btn_start.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.btn_break = tk.Button(
            self.footer,
            text="Start Break",
            bd=5,
            command=self.start_break,
            bg="red",
            font=("arial", 13, "bold"),
        )
        self.btn_break.grid(row=0, column=1, sticky="ew", padx=6)

        self.btn_reset = tk.Button(
            self.footer,
            text="Reset",
            bd=5,
            command=self.reset,
            font=("arial", 13, "bold"),
        )
        self.btn_reset.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    # ------------------------------ Timer logic ------------------------------
    def _set_time(self, remaining_seconds: int):
        minutes, seconds = divmod(max(0, remaining_seconds), 60)
        self.min_var.set(f"{minutes:02d}")
        self.sec_var.set(f"{seconds:02d}")

    # def _play_sound_async(self, path: str = "sound.ogg"):
        # threading.Thread(target=playsound, args=(path,), daemon=True).start()

    def _cancel_after(self):
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _countdown(self, remaining: int):
        self._set_time(remaining)
        if remaining <= 0:
            self._after_id = None
            # self._play_sound_async()
            playsound("sound.ogg")

            if self._mode == "work":
                messagebox.showinfo("Good Job", "Take a break! \nClick 'Start Break'.")
            else:
                messagebox.showinfo("Time's Up", "Get back to work!\n Click 'Start Work'.")
            return

        # schedule next tick
        self._after_id = self.root.after(1000, self._countdown, remaining - 1)

    def start_work(self):
        self._cancel_after()
        self._mode = "work"
        self.mode_label.config(text="Work")
        self._countdown(WORK_MIN * 60)

    def start_break(self):
        self._cancel_after()
        self._mode = "break"
        self.mode_label.config(text="Break")
        self._countdown(SHORT_BREAK_MIN * 60)

    def reset(self):
        self._cancel_after()
        self._mode = "work"
        self.mode_label.config(text="Work")
        self._set_time(WORK_MIN * 60)


def main():
    root = tk.Tk()
    Pomodoro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
