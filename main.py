from playwright.sync_api import sync_playwright
from utils import load_context, load_excel_urls, choose_file
from pages import (
    login,
    buy_now,
    arrival_notification,
    mobile_exclusive,
    out_of_stock,
    unusual_page,
)

if __name__ == "__main__":
    try:
        selected_excel = choose_file()
        print(f"您选择了文件：{selected_excel}")
        urls, maxBuyCounts, indexes = load_excel_urls(selected_excel)
    except Exception as e:
        print(f"加载Excel文件时出错: {e}")
        exit(1)

    with sync_playwright() as playwright:
        # 启动 Chromium 浏览器
        browser = playwright.chromium.launch(headless=False, slow_mo=100, args=["--start-maximized"])

        # 加载上下文
        context = load_context(browser)

        # 新建一个上传图片页面
        upload_page = context.new_page()

        # 创建初始页面,并关闭浏览器的自动化检测
        item_page = context.new_page()
        item_page.add_init_script(
            """Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"""
        )

        # 登陆页面处理
        login(item_page, context)

        # 循环处理每个url
        for url, maxBuyCount, index in zip(urls, maxBuyCounts, indexes):
            # 访问页面
            item_page.goto(url)
            item_page.wait_for_load_state("domcontentloaded")

            if index % 30 == 0:
                print("\n处理30个等待1分钟，避免京东服务器检测到频繁访问")
                item_page.wait_for_timeout(60000)  # 每处理30个商品页面，等待1分钟

            # 检测页面的特殊情况(验证码、账户限制)
            unusual_page(item_page, browser)

            # 开始处理商品页面
            print(
                f"\n---正在打开第 {index-1} 个商品页面, url为{url}, 购买数量为 {maxBuyCount} ---"
            )

            # 检测 "立即购买" 是否存在
            if item_page.locator("xpath=//a[@id='InitTradeUrl']").is_visible():
                print("检测到 '立即购买' 按钮")
                # 定位到输入框并修改值
                item_page.fill("#buy-num", str(maxBuyCount))  # 模拟用户个数
                item_page.wait_for_timeout(1000)  # 等待1秒
                item_page.click("#InitTradeUrl")  # 点击购买按钮
                item_page.wait_for_timeout(1000)  # 等待1秒
                if item_page.url.startswith("https://trade.jd.com/"):
                    print("成功跳转到交易页面")
                    buy_now(item_page, upload_page, index, selected_excel)
                else:
                    print("有购买按钮但是要前往App购买")
                    mobile_exclusive(item_page, upload_page, index, selected_excel)

            # 检测 "到货通知" 或 "售完" 是否存在
            elif (
                item_page.locator("xpath=//a[text()='到货通知']").is_visible()
                or item_page.locator(
                    "xpath=//span[contains(text(), '此商品暂时售完')]"
                ).is_visible()
                or item_page.locator(
                    "xpath=//div[contains(text(), '此商品暂时无货')]"
                ).is_visible()
            ):
                print("检测到 '到货通知' 或 '无货' 按钮")
                arrival_notification(item_page, upload_page, index, selected_excel)

            # 检测 "手机专享" 是否存在
            elif (
                item_page.locator(
                    "xpath=//a[contains(text(), '前往手机购买')]"
                ).is_visible()
                or item_page.locator(
                    "xpath=//div[contains(text(), '仅支持手机扫码购买')]"
                ).is_visible()
            ):
                print("检测到 '前往手机购买' 按钮")
                mobile_exclusive(item_page, upload_page, index, selected_excel)

            # 检测 "缺货" 是否存在
            elif item_page.locator(
                "xpath=//div[@class='itemover-tip']"
            ).is_visible() or item_page.url.startswith("https://www.jd.com/"):
                print("检测到 '该商品已下柜' ")
                out_of_stock(item_page, upload_page, index, selected_excel)

            else:
                print("都未检测到，属于第四种情况，跳过该商品")
                # input("调试中...")
