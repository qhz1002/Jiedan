def two_div_screenshot(page, div1_selector, div2_selector, screenshot_path, padding=2):  
    """  
    对包括两个 <div> 元素进行截图，确保两个div都完整可见  
    :param page: playwright.Page 对象  
    :param div1_selector: 第一个 <div> 元素的 CSS 选择器  
    :param div2_selector: 第二个 <div> 元素的 CSS 选择器  
    :param screenshot_path: 截图保存路径  
    :param padding: 额外的边距空间（像素）  
    """  

    # 定位两个 <div> 
    try: 
        div1 = page.locator(div1_selector)  
        div2 = page.locator(div2_selector)  
    except Exception as e:
        print(f"定位元素失败: {e}")
        return

    # 等待两个 <div> 加载完成  
    div1.wait_for()  
    div2.wait_for()  

    # 获取两个 <div> 的边界框  
    div1_box = div1.bounding_box()  
    div2_box = div2.bounding_box()  

    # 计算需要滚动到的位置  
    # 首先确定垂直方向的滚动范围  
    y_min = min(div1_box['y'], div2_box['y'])  
    y_max = max(div1_box['y'] + div1_box['height'], div2_box['y'] + div2_box['height'])  

    # 计算视口高度  
    viewport_height = page.viewport_size['height']  

    # 计算理想的滚动位置，确保两个div都可见  
    if y_max - y_min > viewport_height:  
        # 如果两个div高度超过视口，选择第一个div的顶部作为参考  
        scroll_to_y = max(0, y_min - padding)  
    else:  
        # 计算居中显示两个div所需的滚动位置  
        center_y = y_min + (y_max - y_min) / 2 - viewport_height / 2  
        scroll_to_y = max(0, center_y)  

    # 使用JavaScript精确滚动  
    page.evaluate(f'window.scrollTo(0, {scroll_to_y})')  

    # 等待滚动和渲染完成  
    page.wait_for_timeout(300)  

    # 重新获取边界框（滚动后可能会变化）  
    div1_box = div1.bounding_box()  
    div2_box = div2.bounding_box()  

    # 计算包含两个 <div> 的最小矩形区域  
    x_min = min(div1_box["x"], div2_box["x"])  
    y_min = min(div1_box["y"], div2_box["y"])  
    x_max = max(div1_box["x"] + div1_box["width"], div2_box["x"] + div2_box["width"])  
    y_max = max(div1_box["y"] + div1_box["height"], div2_box["y"] + div2_box["height"])  

    # 定义截图区域  
    clip = {  
        "x": max(0, x_min - padding),   
        "y": max(0, y_min - padding),   
        "width": x_max - x_min + 2 * padding,   
        "height": y_max - y_min + 2 * padding  
    }  

    # 等待网络空闲  
    page.wait_for_load_state("networkidle")  

    # 对指定区域进行截图  
    try:  
        page.screenshot(path=screenshot_path, clip=clip)  
        print(f"成功截图到 {screenshot_path}")  
    except Exception as e:  
        page.screenshot(path=screenshot_path)  
        print(f"区域截图失败: {e}， 已保存全屏截图到 {screenshot_path}")
