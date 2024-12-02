import flet as ft
import carving_functions

def main(page: ft.Page):
    # functions
    def get_output_dir(e: ft.FilePickerResultEvent):
        if e.path:
            t_output_directory.value = e.path
            t_output_directory.update()
        else:
            "Cancelled"
        return 0

    def get_unallocated_dir(e: ft.FilePickerResultEvent):
        if e.path:
            t_unallocated_dir.value = e.path
            t_unallocated_dir.update()
        else:
            "Cancelled"
        return 0

    def get_file(e: ft.FilePickerResultEvent):
        if e.files:
            t_unallocated_dir.value = e.files[0].path
            t_unallocated_dir.update()
        else:
            "Cancelled"
        return 0

    def carve_files(file, output_directory):
        if not error_handling():  # check for any input errors
            page.window_prevent_close = True  # prevent user from exiting while carving is in progress
            open_dlg_progress()  # display progress ring
            page.update()
            carving_functions.stop_carving = False  # make sure 'stop_carving' is false
            # run the proper file carving function(s) depending on input
            if c_jpeg.value:
                carving_functions.carve_jpeg(file, output_directory)
            if c_png.value:
                carving_functions.carve_png(file, output_directory)
            if c_zip.value:
                carving_functions.carve_zip(file, output_directory)
            page.window_prevent_close = False  # allow user to exit after carving is done
            close_dlg_progress(e=None)  # close progress ring
            page.update()
        return 0

    def open_dlg_progress():
        page.dialog = dlg_progress
        dlg_progress.open = True
        page.update()

    def close_dlg_progress(e):
        carving_functions.stop_carving = True
        page.window_prevent_close = False
        dlg_progress.open = False
        page.update()

    def error_handling():
        page.dialog = dlg_error
        if t_unallocated_dir.value == "":
            dlg_error.content = ft.Text("No unallocated space directory has been selected.")
            dlg_error.open = True
            page.update()
            return True
        elif t_output_directory.value == "":
            dlg_error.content = ft.Text("No output directory has been specified.")
            dlg_error.open = True
            page.update()
            return True
        elif not c_jpeg.value and not c_png.value and not c_zip.value:
            dlg_error.content = ft.Text("No file type has been selected.")
            dlg_error.open = True
            page.update()
            return True
        else:
            return False

    # page settings
    page.title = "File Carver"

    # dialogues
    dlg_pick_dir = ft.FilePicker(on_result=get_output_dir)
    dlg_get_unallocated_dir = ft.FilePicker(on_result=get_unallocated_dir)
    dlg_pick_file = ft.FilePicker(on_result=get_file)
    dlg_progress = ft.AlertDialog(title=ft.Text("Carving in Progress"),
                                  content=ft.ProgressRing(width=25, height=25, stroke_width=2),
                                  actions=[ft.TextButton("Stop Carving", on_click=close_dlg_progress)],
                                  actions_alignment=ft.MainAxisAlignment.CENTER,
                                  modal=True)
    dlg_error = ft.AlertDialog(title=ft.Text("Error"))
    page.overlay.append(dlg_pick_dir)
    page.overlay.append(dlg_get_unallocated_dir)
    page.overlay.append(dlg_pick_file)

    # text fields
    t_unallocated_dir = ft.TextField(label="Unallocated Space Directory", read_only=True)
    t_output_directory = ft.TextField(label="Output directory", read_only=True)

    # buttons
    b_file_select = ft.ElevatedButton(
        text="Select Directory",
        on_click=lambda _: dlg_get_unallocated_dir.get_directory_path()
    )
    b_carve = ft.ElevatedButton(
        text="Carve",
        on_click=lambda _: carve_files(t_unallocated_dir.value, t_output_directory.value),
        height=50, width=150
    )
    b_output_directory = ft.ElevatedButton(
        text="Select Directory",
        on_click=lambda _: dlg_pick_dir.get_directory_path()
    )

    # checkboxes
    c_jpeg = ft.Checkbox(label="JPG")
    c_png = ft.Checkbox(label="PNG")
    c_zip = ft.Checkbox(label="ZIP and Modern Office Files")

    # page display
    page.add(
        ft.Column([
            ft.Row([
                ft.Text("File Carver", size=40)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(padding=10),
            ft.Row([
                t_unallocated_dir,
                b_file_select,
            ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(padding=20),
            ft.Row([
                c_jpeg, c_png, c_zip
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(padding=20),
            ft.Row([
                t_output_directory, b_output_directory
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(padding=20),
            ft.Row([
                b_carve,
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True, alignment=ft.MainAxisAlignment.CENTER)
    )


# run the program
ft.app(target=main)
