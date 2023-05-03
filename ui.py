import customtkinter as ctk
import threading
import os.path
import os
import tkinter as tk
from typing import List, Type
from tkinter import messagebox
import book_handlers
import platformdirs


class LubaProject:
    def __init__(self):
        self.backends: List[Type[book_handlers.models.BookProvider]] = []
        self.backends_dict = {}
        self._current_backend = None
        self._page_offset = "0"
        self._book_url = ""

        self.root = ctk.CTk()
        self.root.title("LubaProject | Download E-Books easy.")
        self.root.geometry("400x240")
        self.root.resizable(False, False)
        self.main_frame = ctk.CTkFrame(master=self.root)

        font = ctk.CTkFont(family="Helvetica", size=40)

        self.title_label = ctk.CTkLabel(
            master=self.root, text="Luba Project", font=font
        )
        self.title_label.pack(pady=10)

        self.other_things_frame = ctk.CTkFrame(self.root)

        self.other_things_frame.pack(pady=5)

        self.backend_var = ctk.StringVar(self.root)
        self.backend_var.set(2)
        self.backend_dropdown = ctk.CTkOptionMenu(
            self.other_things_frame,
            variable=self.backend_var,
            values=[backend.backend_name for backend in self.backends],
            command=self.select_backend,
        )

        self.page_offset_frame = ctk.CTkFrame(self.root)

        self.page_offset_var = ctk.StringVar(value=self._page_offset)
        self.page_offset_field = ctk.CTkEntry(
            self.page_offset_frame,
            textvariable=self.page_offset_var,
            validate="key",
            validatecommand=(self.root.register(self.validate_int), "%P"),
        )

        self.page_offset_button_increment = ctk.CTkButton(
            self.page_offset_frame, text="Increase", command=self.increment_page_offset
        )

        self.page_offset_var_decrease = ctk.CTkButton(
            self.page_offset_frame, text="Decrease", command=self.decrease_page_offset
        )

        self.page_offset_var_autodetect = ctk.CTkButton(
            self.page_offset_frame, text="Autodetect", command=self.toggle_autodetect
        )
        self.page_offset_frame.pack()

        self.page_offset_var_decrease.grid(row=1, column=2)
        self.page_offset_button_increment.grid(row=0, column=2, padx=5, pady=5)
        self.page_offset_field.grid(row=0, column=0, padx=5)
        self.page_offset_var_autodetect.grid(row=1, column=0, pady=5)

        self.book_url_var = ctk.StringVar(value=self._book_url)
        self.book_url_field = ctk.CTkEntry(
            self.other_things_frame,
            textvariable=self.book_url_var,
            validate="key",
            validatecommand=(self.root.register(self.validate_url), "%P"),
        )

        self.book_url_var.set("Please URL here")

        self.book_url_field.bind(
            "<FocusIn>",
            lambda event: self.book_url_field.delete(0, "end")
            if self.book_url_var.get() == "Please URL here"
            else ...,
        )

        self.download_button = ctk.CTkButton(
            self.other_things_frame, text="Download Book", command=self.download_book
        )

        self.settings_button = ctk.CTkButton(
            self.other_things_frame, text="Settings", command=self.show_settings
        )

        self.book_url_field.grid(row=1, column=1, padx=5)
        self.download_button.grid(row=2, column=2)
        self.settings_button.grid(row=1, column=2, padx=5, pady=5)
        self.backend_dropdown.grid(row=2, column=1, pady=5)

    @property
    def current_backend(self) -> Type[book_handlers.BookProvider]:
        return self.backends_dict[self.backend_var.get()]

    @property
    def current_backend_name(self) -> str:
        return self.backend_var.get()

    @property
    def page_offset(self) -> int:
        offset = self.page_offset_var.get()
        if offset == "":
            return 0
        else:
            return int(offset)

    @property
    def book_url(self):
        return self.book_url_var.get()

    @staticmethod
    def toggle_autodetect():
        messagebox.showerror(
            title="Not Implemented", message="This Feature isn't implemented yet!"
        )

    def increment_page_offset(self):
        current_page_offset = self.page_offset + 1
        self.page_offset_var.set(str(current_page_offset))

    def decrease_page_offset(self):
        current_page_offset = self.page_offset - 1
        self.page_offset_var.set(str(current_page_offset))

    def select_backend(self, selection):
        self._current_backend = next(
            (backend for backend in self.backends if backend.backend_name == selection),
            None,
        )

    def show_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        upload_button = ctk.CTkButton(
            settings_window, text="Upload Backend", command=self.upload_backend
        )
        upload_button.pack()

    def add_backend(self, backend: Type[book_handlers.BookProvider]):
        self.backends.append(backend)
        if not backend.backend_name in self.backends_dict.keys():
            self.backends_dict[backend.backend_name] = backend
        self.update_backend_options()

    def update_backend_options(self):
        backend_names = [backend.backend_name for backend in self.backends]
        self.backend_dropdown._values = backend_names
        self.update_options(self.backend_dropdown, new_options=backend_names)

    def update_options(self, optionsmenu: ctk.CTkOptionMenu, new_options: List):
        menu = optionsmenu._dropdown_menu
        # optionsmenu.option_add('test', 'test2')
        menu.delete(0, "end")

        for index, option in enumerate(new_options):
            menu.add_command(
                label=option, command=self.change_backend_wrapper(option=option)
            )  #
            # tk._setit(self.real_backend_var,
            # option)
        optionsmenu.update()

    def change_backend_wrapper(self, option):
        self.backend_var.set(option)
        return tk._setit(self.backend_var, option)

    def upload_backend(self):
        filename = ctk.filedialog.askopenfilename()
        if filename:
            # Select Backend
            ...
            """
            backend = Backend(filename)
            self.backends.append(backend)
            self.backend_dropdown["menu"].delete(0, "end")
            for backend in self.backends:
                self.backend_dropdown["menu"].add_command(
                    label=backend.name,
                    command=tk._setit(self.backend_var, backend.name)
                )
            """

    @staticmethod
    def validate_int(new_value):
        if new_value == "":
            return True
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_url(new_value):
        return True

    def download_book(self):
        if not self.current_backend.get_auth_credentials():
            self.ask_for_credentials()
        if self.book_url == "Please URL here" or self.book_url == "":
            messagebox.showerror(
                "No URL supplied!", "Please enter a valid URL or ID into the URL field."
            )
            return
        messagebox.showinfo(
            "Updating Session Cookie.",
            "Now the Session Cookie is gonna get "
            "refreshed. The program will be "
            "unresponsive in this time. Sadly there "
            "is no workaround to this so just wait it shouldn't take longer than 30 seconds",
        )
        self.current_backend.update_book_ids()

        try:

            self.current_backend.session_cookie
            print('No need to refresh session cookie')
        except AttributeError:
            print('Refreshing Session cookie')
            self.current_backend.update_session_cookie()

        self.download_book_threaded()
        """
        self.current_backend.download_book(
            self.current_backend.extract_identifier(self.book_url),
            download_dir=(
                self.config("download_dir")
                or os.getcwd()
                + "/"
                + self.current_backend.extract_identifier(self.book_url)
            ),
            page_offset=self.page_offset,
            scale=(self.config("scale") or 4),
        )
        """

    def download_book_threaded(self):
        download_thread = threading.Thread(
            target=self.current_backend._download_book,
            # TODO: Implement progressbar with
            #  https://stackoverflow.com/questions/67958976/how-to-thread-a-generator
            args=(self.current_backend.extract_identifier(self.book_url),),
            kwargs={
                "download_dir": (
                    self.config("download_dir")
                    or os.getcwd()
                    + "/"
                    + self.current_backend.extract_identifier(self.book_url)
                ),
                "page_offset": self.page_offset,
                "scale": (self.config("scale") or 4),
            },
        )
        download_thread.start()
        messagebox.showinfo(
            "Download started!",
            "Started the download of the e-Book with the "
            f"ID: {self.current_backend.extract_identifier(self.book_url)}",
        )

    def ask_for_credentials(self):
        password_window, email, password = self.current_backend.ask_for_auth_ui()
        password_window.mainloop()
        # TODO: Add more customizability by adding a list or dictionary and not email/password
        self.current_backend.store_auth_credentials(
            email=email.get(), password=password.get()
        )

    @staticmethod
    def config(keyword: str):
        if filepath := os.path.isfile(
            os.path.join(
                platformdirs.user_config_path("LubaProject", "Flinn"), "config.json"
            )
        ):
            with open(filepath) as f:
                data: dict = json.load(f)
                return data.get(keyword)
        return None

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LubaProject()

    # This part is just here so the app works. It needs atleast two backends to function properly
    # with this frontend solution.
    class test(book_handlers.BookProvider):
        _service_type: str = "test"
        backend_name: str = "DoNotUse"

    app.add_backend(book_handlers.klett.Klett)
    app.add_backend(test)

    # Use this to start the app
    app.start()
