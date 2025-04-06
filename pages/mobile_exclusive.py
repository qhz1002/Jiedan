from utils import two_div_screenshot, write_excel, upload_pic


def mobile_exclusive(page, upload_page, index, selected_excel):

    two_div_screenshot(page, ".preview-wrap", ".itemInfo-wrap", "-2.png")

    # 上传截图获取图片url
    final_url = upload_pic(upload_page, "-2.png")

    # 将生成的url写入excel
    write_excel(selected_excel, index, 9, final_url)
    # 写入 -2 状态
    write_excel(selected_excel, index, 8, -2)
