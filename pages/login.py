def login(page, context, state_file=None):

    # 访问页面
    page.goto("https://www.jd.com/")
    page.wait_for_load_state("networkidle")

    if page.url.startswith("https://cfe.m.jd.com/"):
        print("URL以 'https://cfe.m.jd.com/' 开头，需要过验证码")
        page.wait_for_url("https://www.jd.com/")
        print("登录成功，跳转到首页")

    login_button = page.locator(".link-login")
    print(f"存在登录按钮:{login_button.count()}个")

    while login_button.count() > 0:
        page.goto("https://passport.jd.com/new/login.aspx")
        # 检查 URL 是否以 "https://passport.jd.com/new/login.aspx" 开头
        if page.url.startswith("https://passport.jd.com/new/login.aspx"):
            print("还未登录, 登陆后继续操作")
            while page.url.startswith("https://passport.jd.com/new/login.aspx"):
                page.wait_for_timeout(1000)  # 每秒检查一次，避免占用过多资源
        # 示例操作: 检测到验证，验证跳转后执行检测
        page.wait_for_url("https://www.jd.com/")

    print("登录成功，跳转到首页")

    # 保存上下文登录状态
    if state_file is None:
        state_file = "state.json"
    try:
        context.storage_state(path=state_file)
        print("上下文状态已保存到", state_file)
    except Exception as e:
        print("保存上下文状态失败:", e)
