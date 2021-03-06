# -*- coding: utf-8 -*-
import base64
import time
import subprocess
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def start_background_test_server():
    subprocess.Popen([sys.executable, "./test_server.py"])

def before_all(context):
    context.service = Service('drivers/operadriver')
    context.service.start()
    test_extension = "../restman.nex"

    b64ext = base64.b64encode(open(test_extension, 'rb').read())

    capabilities = {
        'operaOptions': {
            'extensions': [b64ext],
        },
        'Proxy': {
            'proxyType': 'system'
        }
    }
    # Start web server (httpbin FTW!)
    context.server = subprocess.Popen([sys.executable, '-m', 'httpbin.core'])

    # Create browser
    context.browser = webdriver.Remote(context.service.service_url, capabilities)

    # Start extension
    context.browser.switch_to_window(context.browser.window_handles[1])
    context.browser.get('chrome-extension://fohkgjiaiapkkjjchddmhaaaghjakfeg/index.html')
    time.sleep(1)   # Wait for app to load

def after_all(context):
    # Close session
    context.browser.quit()
    time.sleep(0.5)
    context.server.terminate()
