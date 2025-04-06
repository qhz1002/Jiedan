from utils import write_excel, upload_pic, two_div_screenshot


def arrival_notification(page, upload_page, index, selected_excel):

    # 如果有券截图
    quan_item = page.query_selector(".quan-item")
    if quan_item:
        quan_item.click()
        page.wait_for_timeout(1000)
        page.screenshot(path="-1.png")
    else:
        # 如果没有券截图
        two_div_screenshot(page, ".preview-wrap", ".itemInfo-wrap", "-1.png")

    # 上传截图获取图片url
    final_url = upload_pic(upload_page, "-1.png")

    # 将生成的url写入excel
    write_excel(selected_excel, index, 9, final_url)

    # 写入 -1 状态
    write_excel(selected_excel, index, 8, -1)
