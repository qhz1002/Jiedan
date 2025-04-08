import os


def list_excel_files():
    """
    列出当前目录下的所有 .xlsx 文件，并返回文件列表。
    """
    # 获取当前目录下的所有文件
    files = [f for f in os.listdir(".") if f.endswith(".xlsx")]

    if not files:
        print("当前目录下没有找到任何 .xlsx 文件！")
        exit(0)

    # 打印文件列表
    print("当前目录下的 .xlsx 文件：")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    return files


def choose_file():
    """
    让用户选择一个文件，并返回所选文件的路径。

    参数:
        file_list (list): 文件列表。

    返回:
        str: 用户选择的文件名。
    """
    file_list = list_excel_files()
    while True:
        try:
            # 提示用户输入文件编号
            choice = int(input("请输入要处理的文件编号（输入数字，输入0退出）："))
            if choice == 0:
                print("退出程序。")
                exit(0)
            if 1 <= choice <= len(file_list):
                return file_list[choice - 1]
            else:
                print(f"请输入有效的编号（1 到 {len(file_list)}）。")
        except ValueError:
            print("无效输入，请输入数字。")
