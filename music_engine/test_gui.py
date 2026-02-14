#!/usr/bin/env python3

import customtkinter as ctk

def test_gui():
    try:
        print("Creating test window...")
        app = ctk.CTk()
        app.title("Test Window")
        app.geometry("300x200")

        label = ctk.CTkLabel(app, text="Test GUI Window - If you see this, GUI works!")
        label.pack(pady=20)

        button = ctk.CTkButton(app, text="Close", command=app.quit)
        button.pack(pady=10)

        print("Starting mainloop...")
        app.mainloop()
        print("GUI test completed successfully")

    except Exception as e:
        print(f"GUI test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui()