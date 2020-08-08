import sys

from PyQt5.QtWidgets import QApplication

from view.MainView import ViewMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = ViewMainWindow()
    main_window.show()

    sys.exit(app.exec_())
