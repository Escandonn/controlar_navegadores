import multiprocessing
from services.selenium_service import open_chrome, open_firefox


def run_browsers():
    p1 = multiprocessing.Process(target=open_chrome)
    p2 = multiprocessing.Process(target=open_firefox)

    p1.start()
    p2.start()

    p1.join()
    p2.join()