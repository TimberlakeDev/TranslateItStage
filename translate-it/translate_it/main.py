import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def open_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--force-dark-mode")
    options.add_argument("--force-device-scale-factor=4")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    # Moving right and up from primary display, adjust as necessary.
    driver.set_window_position(300, -250)
    sleep(1)
    driver.maximize_window()
    sleep(1)

    return driver


def apply_dark_mode(driver):
    dark_mode_css = """
    document.documentElement.style.filter = 'invert(1) hue-rotate(180deg)';
    document.querySelectorAll('img, video').forEach(elem => elem.style.filter = 'invert(1) hue-rotate(180deg)');
    """
    driver.execute_script(dark_mode_css)


def open_website(driver):
    driver.get("https://translate.it/")

    code = input("Enter the conversation code: ")
    driver.find_element(
        By.CSS_SELECTOR, "input[aria-label='Enter 5 letter conversation code']"
    ).send_keys(code)

    now = datetime.datetime.now()
    driver.find_element(By.CSS_SELECTOR, "input[aria-label='Username']").send_keys(
        "TimberlakeK" + str(int(now.timestamp()))[-4:-1]
    )
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    apply_dark_mode(driver)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "messageList")))
    # hits the f11 key to go fullscreen
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F11)

    script = """
    document.body.style.visibility = 'hidden';

    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = '.userIconContainer { display: none !important; }';
    style.innerHTML += '.messageContent { box-shadow: none; max-width: 100% !important;}';
    style.innerHTML += '.messageContainer { max-width: 100% !important; padding-block: 0.5em !important;}';
    style.innerHTML += '.username { display: none !important; }';
    document.getElementsByTagName('head')[0].appendChild(style);


    var messageList = document.querySelector('.messageList');
    if (messageList) {
        messageList.style.visibility = 'visible';

        messageList.style.position = 'fixed'; // Position it relative to the viewport
        messageList.style.zIndex = '9999'; // Ensure it's on top
        messageList.style.top = '0'; // Align top edge with the viewport
        messageList.style.left = '0'; // Align left edge with the viewport
        messageList.style.width = '100vw'; // Stretch to full viewport width
        messageList.style.height = '100vh'; // Stretch to full viewport height
        messageList.style.overflow = 'auto'; // Add scrollbars if content overflows
        messageList.style.background = 'white'; // Ensure readability with a solid background
        messageList.style.margin = '0'; // Remove any default margins

        var makeChildrenVisible = function(element) {
            Array.from(element.children).forEach(function(child) {
                child.style.visibility = 'visible';
                makeChildrenVisible(child); // Apply recursively
            });
        };
        makeChildrenVisible(messageList);
    }
    """
    driver.execute_script(script)
    driver.fullscreen_window()


if __name__ == "__main__":
    while True:
        driver = open_webdriver()
        open_website(driver)

        userInput = input("Press Enter to create a new session or type 'q' to quit: ")

        driver.quit()

        if userInput == "q":
            break
