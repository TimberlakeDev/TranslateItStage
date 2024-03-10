from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# import WebDriverWait from selenium.webdriver.support.ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    options.add_argument("--disable-infobars")
    options.add_argument("--force-dark-mode")
    options.add_argument("--force-device-scale-factor=3")
    options.add_argument("--hide-scrollbars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

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

    driver.find_element(By.CSS_SELECTOR, "input[aria-label='Username']").send_keys(
        "Timberlake"
    )
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    apply_dark_mode(driver)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "messageList")))

    script = """
    document.body.style.visibility = 'hidden';

    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = '.userIconContainer { display: none !important; }';
    style.innerHTML += '.messageContent { box-shadow: none; }';
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

    sleep(86400)


if __name__ == "__main__":
    driver = open_webdriver()
    open_website(driver)
    driver.quit()
