from seleniumbase import SB


def open_chrome():
    with SB(browser="chrome", headed=True) as sb:
        sb.open("https://www.google.com")
        sb.sleep(5)


def open_firefox():
    with SB(browser="firefox", headed=True) as sb:
        sb.open("https://www.bing.com")
        sb.sleep(5)