import sys
from PyQt5.QtWidgets import QApplication

from presentation.dashboard_window import DashboardWindow
from controller.app_controller import AppController


def main():
    app = QApplication(sys.argv)

    controller = AppController()
    window = DashboardWindow(controller)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()

