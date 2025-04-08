import os


def unusual_page(page, browser):

    # 检测是否需要过验证
    if page.url.startswith("https://cfe.m.jd.com/"):
        print("URL以 'https://cfe.m.jd.com/' 开头，需要手动通过验证码")
        print("请在浏览器中手动完成验证码验证，完成后页面会自动跳转")

        # 等待页面跳转到非验证码页面
        while page.url.startswith("https://cfe.m.jd.com/"):
            page.wait_for_timeout(1000)  # 每秒检查一次，避免占用过多资源

        print("验证成功，跳转到商品页:", page.url)
        page.goto(page.url)

    # 检测是否被限制
    elif page.url.startswith(
        "https://www.jd.com/?from=pc_item&reason=403"
    ) or page.url.startswith("https://www.jd.com/?from=pc_item_sd"):
        print("账号已被限制，请重新登录")
        browser.close()
        while True:
            try:
                choice = int(
                    input(
                        "是否删除登录信息？(输入 0 回车删除, 直接回车不删除退出程序): "
                    )
                )
                if choice == 0:
                    os.remove("state.json")
                    print("已删除登录信息，请重新运行程序")
                    exit(1)
                else:
                    print("程序退出")
                    exit(1)
            except ValueError:
                print("程序退出")
                exit(1)
