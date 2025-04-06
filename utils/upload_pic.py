def upload_pic(upload_page, file_name):

    upload_page.goto("http://106.13.59.243/zeus/apps/treasure/upload")

    # 输入token
    upload_page.locator('input[placeholder="请输入token"]').fill(
        "18bb0ad9-dfbf-4f12-b6c8-543b4e155caa"
    )

    try:
        # 定位到文件上传的 input 元素
        file_input = upload_page.locator('input[name="file"]')
        # 确保文件上传区域可见（如果需要）
        upload_area = upload_page.locator(".ant-upload-drag-container")
        upload_area.scroll_into_view_if_needed()
        # 上传文件
        file_input.set_input_files(file_name)

        print(f"{file_name}已成功上传.")
    except Exception as e:
        print("上传文件失败:", e)

    # 使用 XPath 定位包含文本 "上 传" 的按钮
    upload_button = upload_page.locator("xpath=//button[span[text()='上 传']]")
    upload_button.click()  # 点击按钮

    # 获取生成的url并返回
    final_url = upload_page.locator(
        "xpath=//div[@class='style-hintInfo--Pbq0n']"
    ).inner_text()

    return final_url
