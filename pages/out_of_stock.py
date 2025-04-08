from utils import two_div_screenshot, write_excel, upload_pic


def out_of_stock(page, upload_page, index, selected_excel):

    if page.url.startswith("https://www.jd.com/"):
        # 跳转到首页截图
        page.screenshot(path="image.png")
    else:
        # 商品截图
        two_div_screenshot(page, ".preview-wrap", ".itemInfo-wrap", "image.png")

    # 上传截图获取图片url
    final_url = upload_pic(upload_page, "image.png")

    # 将生成的url写入excel
    write_excel(selected_excel, index, 9, final_url)
    # 写入 -3 状态
    write_excel(selected_excel, index, 8, -3)
