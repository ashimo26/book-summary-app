# main.py
from ui.gradio_ui import create_ui
import config

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(debug=True)
