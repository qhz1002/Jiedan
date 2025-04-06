import os
import pandas as pd


def list_excel_files():
    """
    列出当前目录下的所有 .xlsx 文件，并返回文件列表。
    """
    # 获取当前目录下的所有文件
    files = [f for f in os.listdir(".") if f.endswith(".xlsx")]

    if not files:
        print("当前目录下没有找到任何 .xlsx 文件！")
        return None

    # 打印文件列表
    print("当前目录下的 .xlsx 文件：")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    return files


def choose_file(file_list):
    """
    让用户选择一个文件，并返回所选文件的路径。

    参数:
        file_list (list): 文件列表。

    返回:
        str: 用户选择的文件名。
    """
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


def split_excel_by_rows(input_file, output_prefix, rows_per_file=200):
    """
    将一个 Excel 文件按指定行数拆分为多个文件。

    参数:
        input_file (str): 输入的 Excel 文件路径。
        output_prefix (str): 输出文件的前缀名称。
        rows_per_file (int): 每个文件包含的行数，默认为 200。
    """
    # 读取 Excel 文件
    df = pd.read_excel(input_file)

    # 获取总行数
    total_rows = len(df)

    # 计算需要拆分的文件数量
    num_files = (total_rows // rows_per_file) + (
        1 if total_rows % rows_per_file != 0 else 0
    )

    print(f"总行数: {total_rows}, 需要拆分成 {num_files} 个文件")

    # 按行数拆分并保存
    for i in range(num_files):
        start_row = i * rows_per_file
        end_row = min((i + 1) * rows_per_file, total_rows)

        # 提取当前分片的数据
        chunk = df.iloc[start_row:end_row]

        # 构造输出文件名
        output_file = f"{output_prefix}_part{i+1}.xlsx"

        # 保存到新的 Excel 文件
        chunk.to_excel(output_file, index=False)
        print(f"已保存文件: {output_file} (行范围: {start_row}-{end_row-1})")


# 主程序
if __name__ == "__main__":
    # 列出当前目录下的所有 .xlsx 文件
    excel_files = list_excel_files()

    if excel_files:
        # 让用户选择文件
        selected_file = choose_file(excel_files)
        print(f"您选择了文件: {selected_file}")

        # 设置输出文件前缀
        output_prefix = input("请输入输出文件的前缀名称（如 output_file）：").strip()

        # 调用拆分函数
        split_excel_by_rows(selected_file, output_prefix, rows_per_file=200)
