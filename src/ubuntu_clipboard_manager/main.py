from .gui.main_window import MainWindow
from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')


def main():
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
