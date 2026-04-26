import multiprocessing

from infrastructure.selenium.selenium_service import open_chrome, open_firefox


def run_browsers():
    """Ejecuta cada navegador en un proceso separado."""
    processes = [
        multiprocessing.Process(target=open_chrome),
        multiprocessing.Process(target=open_firefox),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
