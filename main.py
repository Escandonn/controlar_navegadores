import sys
from PyQt5.QtWidgets import QApplication

from presentation.main_window import MainWindow
from controller.app_controller import AppController


def main():
    app = QApplication(sys.argv)

    controller = AppController()
    window = MainWindow(controller)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()

