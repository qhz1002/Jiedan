def take_screenshot(page, div_start, div_end, file_name):
    if div_start and div_end:
        # 使用 page.evaluate() 获取 start_box 的绝对坐标
        start_box = page.evaluate(
            """element => {
            const rect = element.getBoundingClientRect();
            return {
                x: rect.x + window.scrollX,       // 绝对 x 坐标
                y: rect.y + window.scrollY,       // 绝对 y 坐标
                width: rect.width,                // 宽度
                height: rect.height               // 高度
            };
        }""",
            div_start,
        )

        # 使用 page.evaluate() 获取 end_box 的绝对坐标
        end_box = page.evaluate(
            """element => {
            const rect = element.getBoundingClientRect();
            return {
                x: rect.x + window.scrollX,       // 绝对 x 坐标
                y: rect.y + window.scrollY,       // 绝对 y 坐标
                width: rect.width,                // 宽度
                height: rect.height               // 高度
            };
        }""",
            div_end,
        )

        if start_box and end_box:
            # 计算包含两个元素的最小矩形区域
            x_min = min(start_box["x"], end_box["x"])
            y_min = min(start_box["y"], end_box["y"])
            x_max = max(
                start_box["x"] + start_box["width"], end_box["x"] + end_box["width"]
            )
            y_max = max(
                start_box["y"] + start_box["height"], end_box["y"] + end_box["height"]
            )

            clip_region = {
                "x": x_min,
                "y": y_min,
                "width": x_max - x_min,
                "height": y_max - y_min,
            }

            # 对计算出的区域进行截图
            page.screenshot(
                path=file_name, clip=clip_region  # 保存截图的文件路径  # 指定截图区域
            )
            print(f"已保存截图'{file_name}'.")
        else:
            print("未找到边缘.")
    else:
        print("没有开始和结束div元素.")
        page.screenshot(path=file_name)
