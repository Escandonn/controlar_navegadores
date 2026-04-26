from core.config import CHROME_URL, FIREFOX_URL
from seleniumbase import SB


def open_chrome():
    with SB(browser="chrome", headed=True) as sb:
        sb.open(CHROME_URL)
        sb.sleep(5)


def open_firefox():
    with SB(browser="firefox", headed=True) as sb:
        sb.open(FIREFOX_URL)
        sb.sleep(5)
