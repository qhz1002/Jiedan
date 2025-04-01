import os
import json
from playwright.sync_api import Playwright, sync_playwright, expect

# 定义存储上下文数据的路径
CONTEXT_STORAGE_PATH = "browser_context_storage.json"

def load_context(context):
    """
    加载已有的上下文数据（如 cookies、localStorage 等）。
    """
    if os.path.exists(CONTEXT_STORAGE_PATH):
        with open(CONTEXT_STORAGE_PATH, "r") as f:
            storage_state = json.load(f)
        context.add_cookies(storage_state.get("cookies", []))
        print("Loaded existing browser context.")
    else:
        print("No existing browser context found.")

def save_context(context):
    """
    保存当前的上下文数据（如 cookies、localStorage 等）。
    """
    storage_state = context.storage_state()
    with open(CONTEXT_STORAGE_PATH, "w") as f:
        json.dump(storage_state, f)
    print("Browser context saved successfully.")

def run(playwright: Playwright) -> None:
    # 启动浏览器（非无头模式）
    browser = playwright.chromium.launch(
    headless=False  # 设置 headless=False 可以看到浏览器界面
    )

    # 创建一个新的上下文，并模拟普通浏览器信息
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1280},  # 设置屏幕分辨率
        locale="zh-CN",  # 设置语言
        geolocation={"latitude": 39.9042, "longitude": 116.4074},  # 模拟地理位置（可选）
        permissions=["geolocation"],  # 授予地理位置权限（可选）
    )

    # 加载已有的上下文数据
    load_context(context)

    # 打开一个新页面
    page = context.new_page()

    page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
""")

    # 打开目标页面
    page.goto("https://item.jd.com/10077319962594.html")
    print("Browser is running. Close the browser window manually to exit.")

    # 定位到输入框并修改值
    input_selector = "#buy-num"  # 使用 ID 定位
    page.fill(input_selector, "2")  # 直接设置值为 2
    
    page.click(".btn-special2.btn-lg")  # 点击按钮
    
    page.wait_for_timeout(3000)  # 等待 2 秒以确保页面加载完成

    div_start = page.wait_for_selector("xpath=(//div[@class='step-tit'])[4]")
    div_end = page.wait_for_selector("xpath=//div[@id='checkout-floatbar']")    
    print("Div Start:", div_start)
    print("Div End:", div_end)

    if div_start and div_end:
        # 使用 page.evaluate() 获取 start_box 的绝对坐标
        start_box = page.evaluate("""element => {
            const rect = element.getBoundingClientRect();
            return {
                x: rect.x + window.scrollX,       // 绝对 x 坐标
                y: rect.y + window.scrollY,       // 绝对 y 坐标
                width: rect.width,                // 宽度
                height: rect.height               // 高度
            };
        }""", div_start)

        # 使用 page.evaluate() 获取 end_box 的绝对坐标
        end_box = page.evaluate("""element => {
            const rect = element.getBoundingClientRect();
            return {
                x: rect.x + window.scrollX,       // 绝对 x 坐标
                y: rect.y + window.scrollY,       // 绝对 y 坐标
                width: rect.width,                // 宽度
                height: rect.height               // 高度
            };
        }""", div_end)
        

        if start_box and end_box:
            # 计算包含两个元素的最小矩形区域
            x_min = min(start_box["x"], end_box["x"])
            y_min = min(start_box["y"], end_box["y"])
            x_max = max(start_box["x"] + start_box["width"], end_box["x"] + end_box["width"])
            y_max = max(start_box["y"] + start_box["height"], end_box["y"] + end_box["height"])

            clip_region = {
                "x": x_min,
                "y": y_min,
                "width": x_max - x_min,
                "height": y_max - y_min
            }

            # 对计算出的区域进行截图
            page.screenshot(
                path="div_range_screenshot.png",  # 保存截图的文件路径
                clip=clip_region  # 指定截图区域
            )
            print("Screenshot of the specified div range saved as 'div_range_screenshot.png'.")
        else:
            print("One or both elements' bounding boxes not found.")
    else:
        print("One or both elements not found.")

    # 保持运行，直到用户手动关闭浏览器
    try:
        while browser.is_connected():
            page.wait_for_timeout(1000)  # 每秒检查一次浏览器状态
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Closing browser...")
    finally:
        # 保存上下文数据
        save_context(context)

        # 确保资源被正确清理（即使用户强制退出）
        context.close()
        browser.close()

# 使用 Playwright 运行脚本
with sync_playwright() as playwright:
    run(playwright)