import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
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


if __name__ == '__main__':
    PotatoApp().run()
