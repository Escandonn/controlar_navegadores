from workers.browser_worker import run_browsers


class AppController:

    def start_browsers(self):
        run_browsers()