#!/usr/bin/env python3
import asyncio
import json
import os
from playwright.async_api import async_playwright

NSTBROWSER_WS_URL = os.environ.get('NSTBROWSER_URL', 'ws://localhost:8848/ws/connect')
USERNAME = os.environ.get('EASYHITS4U_USERNAME', 'clarabassoni2+borevunechi@gmail.com')
PASSWORD = os.environ.get('EASYHITS4U_PASSWORD', 'ZAmena24')

async def login():
    async with async_playwright() as p:
        print("🔄 Connessione a Nstbrowser...")
        browser = await p.chromium.connect_over_cdp(NSTBROWSER_WS_URL)
        page = await browser.new_page()
        
        print("📡 EasyHits4U login...")
        await page.goto("https://www.easyhits4u.com/logon/")
        await page.wait_for_selector('input[name="username"]', timeout=30000)
        
        await page.fill('input[name="username"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button.btn_green')
        
        await page.wait_for_url(lambda url: "member" in url, timeout=30000)
        
        cookies = await page.context.cookies()
        print("✅ Login OK!")
        
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(login())