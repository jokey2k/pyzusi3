import functools
import logging
import sys

from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

#logging.basicConfig(level=logging.INFO)
#logging.getLogger("pyzusi3.messagecoders.MessageDecoder").setLevel(logging.DEBUG)

# Important:
# You need to run the following command to (re)generate the form_ui.py file
#     pyside6-uic form.ui -o form_ui.py

def main():
    app = QApplication(sys.argv)

    app.setApplicationName("AutoSifa")
    app.setOrganizationName("MarkusUllmann")

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()
    sys.exit()

if __name__ == "__main__":
    main()