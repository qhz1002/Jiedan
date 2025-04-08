import json


def load_context(browser, state_file=None, **kwargs):
    """
    加载或创建浏览器上下文。

    参数:
        browser: Playwright 的浏览器实例。
        state_file: 保存上下文状态的文件路径，默认为 "data/state.json"。
        **kwargs: 可选参数，用于设置上下文的默认配置（如 viewport、user_agent 等）。

    返回:
        BrowserContext 对象。
    """
    if state_file is None:
        state_file = "state.json"

    try:
        # 尝试加载保存的上下文状态
        with open(state_file) as f:
            storage_state = json.load(f)
        context = browser.new_context(
            storage_state=storage_state, viewport={"width": 1920, "height": 1280}
        )
        print("已加载保存的登录状态")
    except FileNotFoundError:
        # 如果未找到保存的状态文件，创建新的上下文
        default_kwargs = {
            "viewport": {"width": 1920, "height": 1280},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "locale": "zh-CN",
            "timezone_id": "Asia/Shanghai",
        }
        # 合并默认参数和用户传入的参数
        final_kwargs = {**default_kwargs, **kwargs}
        context = browser.new_context(**final_kwargs)
        print("未找到保存的登录状态，创建新的登录状态")

    return context
