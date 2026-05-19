import threading
import time
from flask import Flask
import dashboard_server
from playwright.sync_api import sync_playwright
import os
import signal

def run_server():
    # Start internal flask server that dashboard_server provides
    # But dashboard_server uses __main__ to run, so we can just use its app
    dashboard_server.app.run(port=5000, use_reloader=False)

def take_shot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000', wait_until='networkidle')
        
        # Click on start sim 
        page.click('button#runBtn')
        
        # Wait for 3 seconds for simulation to spread some cars
        time.sleep(3)
        
        # Take screenshot
        page.screenshot(path='dashboard_gorseli.png')
        browser.close()

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    # Wait for server to start
    time.sleep(2)
    take_shot()
    print("Dashboard PNG basariyla alindi!")
    os._exit(0)
