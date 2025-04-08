from utils import write_excel, upload_pic, two_div_screenshot


def arrival_notification(page, upload_page, index, selected_excel):
    # 等待页面加载完毕
    page.wait_for_load_state("networkidle")  # 等待网络空闲状态
    
    # 如果有券截图
    quan_item = page.locator(".quan-item")
    
    if quan_item.count() > 0:  # 如果存在 .quan-item
            try:
                quan_item.wait_for(timeout=5000)  # 等待元素可见，最多 5 秒
                quan_item.click()
                print("成功点击 .quan-item")
                page.wait_for_timeout(1000)
                page.screenshot(path="image.png")
            except TimeoutError:
                print("等待 .quan-item 超时，可能不可点击")
    else:
        print("没有优惠券，执行下一步")
        two_div_screenshot(page, ".preview-wrap", ".itemInfo-wrap", "image.png")

    # 上传截图获取图片url
    final_url = upload_pic(upload_page, "image.png")

    # 将生成的url写入excel
    write_excel(selected_excel, index, 9, final_url)

    # 写入 -1 状态
    write_excel(selected_excel, index, 8, -1)
