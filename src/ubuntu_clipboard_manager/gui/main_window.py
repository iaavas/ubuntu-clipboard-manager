from ..clipboard.manager import ClipboardManager
from gi.repository import Gtk, Gdk, GdkPixbuf
import gi
gi.require_version('Gtk', '3.0')


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ubuntu Clipboard Manager")
        self.set_border_width(10)
        self.set_default_size(300, 400)

        self.clipboard_manager = ClipboardManager()
        self.clipboard_manager.start_monitoring()

        self.create_ui()

    def create_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self.on_row_activated)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.listbox)
        vbox.pack_start(scrolled_window, True, True, 0)

        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.connect("clicked", self.on_refresh_clicked)
        vbox.pack_start(refresh_button, False, False, 0)

        self.update_history()

    def update_history(self):
        for child in self.listbox.get_children():
            self.listbox.remove(child)

        for item in self.clipboard_manager.get_history():
            if item.is_image:
                image = Gtk.Image.new_from_pixbuf(
                    item.content.scale_simple(50, 50, GdkPixbuf.InterpType.BILINEAR))
                self.listbox.add(image)
            else:
                label = Gtk.Label(label=item.content)
                label.set_line_wrap(True)
                label.set_max_width_chars(30)
                self.listbox.add(label)

        self.listbox.show_all()

    def on_refresh_clicked(self, widget):
        self.update_history()

    def on_row_activated(self, listbox, row):
        index = row.get_index()
        item = self.clipboard_manager.get_history()[index]
        self.clipboard_manager.set_clipboard_content(item)
