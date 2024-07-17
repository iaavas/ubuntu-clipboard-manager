import time
from collections import deque
from gi.repository import Gtk, Gdk, GdkPixbuf
import gi
gi.require_version('Gtk', '3.0')


class ClipboardItem:
    def __init__(self, content, is_image=False):
        self.content = content
        self.is_image = is_image
        self.timestamp = time.time()


class ClipboardManager:
    def __init__(self, max_items=20):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.history = deque(maxlen=max_items)

    def start_monitoring(self):
        self.clipboard.connect('owner-change', self.on_clipboard_change)

    def on_clipboard_change(self, clipboard, event):
        if clipboard.wait_is_image_available():
            image = clipboard.wait_for_image()
            if image:
                self.save_to_history(image, is_image=True)
        else:
            text = clipboard.wait_for_text()
            if text:
                self.save_to_history(text)

    def save_to_history(self, content, is_image=False):
        item = ClipboardItem(content, is_image)
        self.history.appendleft(item)

    def get_history(self):
        return list(self.history)

    def set_clipboard_content(self, item):
        if item.is_image:
            self.clipboard.set_image(item.content)
        else:
            self.clipboard.set_text(item.content, -1)
