import functools
import logging
import sys

from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

#logging.basicConfig(level=logging.INFO)

# Important:
# You need to run the following command to (re)generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py

def main():
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()
    sys.exit()

if __name__ == "__main__":
    main()