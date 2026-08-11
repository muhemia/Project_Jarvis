import customtkinter as ctk


class SmartCamApp(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__()

        self.title("Project Jarvis - Smart Cam with AI")
        self.geometry("720x420")
        self.minsize(520, 320)
        self.configure(fg_color="#101418")

        title_label = ctk.CTkLabel(
            self,
            text="Project Jarvis - Smart Cam with AI",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#f5f7fb",
        )
        title_label.place(relx=0.5, rely=0.16, anchor="center")

        start_button = ctk.CTkButton(
            self,
            text="Start Camera",
            command=self.on_start_camera_click,
            width=240,
            height=64,
            corner_radius=16,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="#ffffff",
            font=ctk.CTkFont(size=19, weight="bold"),
        )
        start_button.place(relx=0.5, rely=0.48, anchor="center")

        close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.close_window,
            width=240,
            height=52,
            corner_radius=16,
            fg_color="#374151",
            hover_color="#4b5563",
            text_color="#ffffff",
            font=ctk.CTkFont(size=17, weight="bold"),
        )
        close_button.place(relx=0.5, rely=0.66, anchor="center")

        self.result = False

    # gibt true zurück, wenn start gedrückt wird
    def on_start_camera_click(self):
        self.result = True 
        print("Kamera wurde gestartet!")
        self.withdraw()
        self.quit()

    # gibt false zurück, wenn close gedrückt wird
    def close_window(self):
        self.result = False
        print("System wurde erfolgreich beendet! Bis zum nächsten mal!")
        self.quit()


def frontend():
    app = SmartCamApp()
    app.deiconify()   # verstecktes Fenster wieder anzeigen
    app.mainloop()
    return app.result


if __name__ == "__main__":
    frontend()
