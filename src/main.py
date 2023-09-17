from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()


@app.get("/playwright")
async def playwright_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://whatsmyuseragent.org/")
        await browser.close()
    return {"Hello": "World"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
