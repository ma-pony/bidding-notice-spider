from html import unescape

from fastapi import FastAPI
from parsel import Selector
from playwright.async_api import async_playwright

app = FastAPI()


def remove_tags_and_attribs(content: str):
    """
    删除标签及其属性
    :param content:
    :return:
    """
    html = Selector(unescape(content))
    for element in html.xpath("//*"):
        element.root.attrib.clear()
        if element.root.tag in ["script", "style"]:
            element.drop()

    return html.get()


async def route_handler(route, request):
    """
    拦截请求，过滤图片和视频请求
    :param route:
    :param request:
    :return:
    """
    if request.resource_type in ["image", "media"]:
        await route.abort()
    else:
        await route.continue_()


browser_args = [
    "--disable-web-security",
    "--disable-extensions",
    "--disable-sync",
    "--disable-setuid-sandbox",
    "--no-first-run",
    "--no-sandbox",
    "--ignore-certificate-errors",
    "--disable-blink-features=AutomationControlled",
    "--user-agent=\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36\"",
]


@app.get("/playwright")
async def playwright_page(url: str = "https://www.baidu.com"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=browser_args,
        )
        context = await browser.new_context()
        page = await context.new_page()
        await page.route("**/*", route_handler)
        await page.goto(url)
        content = await page.content()
        content = remove_tags_and_attribs(content)
        await page.close()
        await browser.close()
    return content


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
