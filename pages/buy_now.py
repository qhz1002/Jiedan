from utils import write_excel, upload_pic, two_div_screenshot


def buy_now(page, upload_page, index, selected_excel):

    # 定位截图
    div_start = "xpath=(//div[@class='step-tit'])[4]"
    div_end = "xpath=//div[@id='checkout-floatbar']"
     
    two_div_screenshot(page, div_start, div_end, "1.png")

    # 上传截图获取图片url
    final_url = upload_pic(upload_page, "1.png")

    # 将生成的url写入excel
    write_excel(selected_excel, index, 9, final_url)
    # 写入 1 状态
    write_excel(selected_excel, index, 8, 1)
