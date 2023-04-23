import customtkinter as ctk
import tkinter as tk
from typing import List, Type
import book_handlers


class LubaProject:
    def __init__(self):
        self.backends: List[Type[book_handlers.models.BookProvider]] = []
        self.backends_dict = {}
        self.current_backend = None
        self.page_offset = 0
        self.book_url = ""

        self.root = ctk.CTk()
        self.root.title('LubaProject | Download E-Books easy.')
        self.root.geometry("400x240")
        self.main_frame = ctk.CTkFrame(master=self.root)

        self.backend_var = ctk.StringVar(self.root)
        self.backend_var.set(2)
        self.real_backend_var = ctk.StringVar()
        self.backend_dropdown = ctk.CTkOptionMenu(
            self.root,
            variable=self.backend_var,
            values=[backend.backend_name for backend in self.backends],
            command=self.select_backend
        )
        self.backend_dropdown.pack()

        self.page_offset_var = ctk.IntVar(value=self.page_offset)
        self.page_offset_field = ctk.CTkEntry(
            self.root,
            textvariable=self.page_offset_var,
            validate="key",
            validatecommand=(self.root.register(self.validate_int), "%P")
        )
        self.page_offset_field.pack()

        self.book_url_var = ctk.StringVar(value=self.book_url)
        self.book_url_field = ctk.CTkEntry(
            self.root,
            textvariable=self.book_url_var,
            validate="key",
            validatecommand=(self.root.register(self.validate_url), "%P")
        )
        self.book_url_field.pack()

        self.download_button = ctk.CTkButton(
            self.root,
            text="Download Book",
            command=self.download_book
        )
        self.download_button.pack()

        self.settings_button = ctk.CTkButton(
            self.root,
            text="Settings",
            command=self.show_settings
        )
        self.settings_button.pack()

    def select_backend(self, selection):
        self.current_backend = next(
            (backend for backend in self.backends if backend.backend_name == selection), None)

    def show_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        upload_button = ctk.CTkButton(
            settings_window,
            text="Upload Backend",
            command=self.upload_backend
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
        menu.delete(0, 'end')

        for index, option in enumerate(new_options):
            menu.add_command(label=option, command=self.change_backend_wrapper(option=option))  #
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
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_url(new_value):
        return True

    def download_book(self):
        print('######')
        print(self.backend_var.get())
        print('######')


if __name__ == '__main__':
    app = LubaProject()


    class test(book_handlers.BookProvider):
        _service_type: str = "test"
        backend_name: str = "TestBackend"


    app.add_backend(book_handlers.klett.Klett)
    app.add_backend(test)
    print(app.backends)
    # app.update_backend_options()
    app.root.mainloop()
