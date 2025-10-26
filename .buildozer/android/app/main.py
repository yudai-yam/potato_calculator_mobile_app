import os
import sys
import shutil
from pathlib import Path
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from utils import save_sales, calculate_price

# Ensure backend package is importable when running from repository root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BACKEND_SRC = os.path.join(ROOT, 'backend', 'src')
if BACKEND_SRC not in sys.path:
    sys.path.insert(0, BACKEND_SRC)



KV = os.path.join(os.path.dirname(__file__), 'calculator.kv')
Builder.load_file(KV)


class PotatoApp(App):
    def build(self):
        # On desktop, set a reasonable window size for testing
        Window.size = (360, 640)
        return Builder.load_file(KV)

    def calculate(self):
        try:
            grams_text = self.root.ids.grams_input.text.strip()
            if not grams_text:
                self.root.ids.result_label.text = "Please enter grams"
                return
            grams = float(grams_text)
            price = calculate_price(grams)
            save_sales(int(grams), price) 
            self.root.ids.result_label.text = f"Price: {price}"
        except ValueError:
            self.root.ids.result_label.text = "Invalid number"
        except Exception as e:
            self.root.ids.result_label.text = f"Error: {e}"

    def _find_sales_csv(self) -> Path | None:
        """Try to locate the project's sales.csv file in several likely places."""
        candidates = [
            Path(os.getcwd()) / 'sales.csv',
            Path(__file__).resolve().parents[1] / 'sales.csv',
            Path(__file__).resolve().parent / 'sales.csv',
        ]

        for p in candidates:
            if p.exists():
                return p

        # Fallback: search up to 3 levels up from this file for sales.csv
        root = Path(__file__).resolve().parents[2]
        for dirpath, dirnames, filenames in os.walk(root):
            if 'sales.csv' in filenames:
                return Path(dirpath) / 'sales.csv'

        return None

    def open_export_popup(self):
        """Open a popup that lets the user select a directory and filename to export sales.csv."""
        src = self._find_sales_csv()
        if not src:
            popup = Popup(title='Export CSV', content=Label(text='sales.csv not found.'), size_hint=(0.6, 0.3))
            popup.open()
            return

        # Build popup UI
        content = BoxLayout(orientation='vertical', spacing=8, padding=8)
        filechooser = FileChooserListView(path=str(Path.home()), dirselect=True)
        filename_input = TextInput(text='sales.csv', size_hint_y=None, height='36dp')
        status_label = Label(text='Choose directory and filename then tap Save', size_hint_y=None, height='24dp')

        btns = BoxLayout(size_hint_y=None, height='44dp', spacing=8)
        save_btn = Button(text='Save')
        cancel_btn = Button(text='Cancel')
        btns.add_widget(save_btn)
        btns.add_widget(cancel_btn)

        content.add_widget(filechooser)
        content.add_widget(filename_input)
        content.add_widget(status_label)
        content.add_widget(btns)

        popup = Popup(title='Export sales.csv', content=content, size_hint=(0.9, 0.9))

        def do_save(instance):
            dest_dir = Path(filechooser.path)
            if not dest_dir.exists() or not dest_dir.is_dir():
                status_label.text = f'Invalid destination: {dest_dir}'
                return

            dest_file = dest_dir / filename_input.text.strip()
            try:
                shutil.copyfile(src, dest_file)
                status_label.text = f'Saved to {dest_file}'
            except Exception as ex:
                status_label.text = f'Error: {ex}'
            else:
                # keep the popup briefly so user sees success; close after a short delay
                from kivy.clock import Clock

                def close_it(dt):
                    popup.dismiss()

                Clock.schedule_once(close_it, 0.9)

        def do_cancel(instance):
            popup.dismiss()

        save_btn.bind(on_release=do_save)
        cancel_btn.bind(on_release=do_cancel)

        popup.open()


if __name__ == '__main__':
    PotatoApp().run()
