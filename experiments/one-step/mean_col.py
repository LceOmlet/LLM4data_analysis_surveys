import pandas as pd
import numpy as np

def calculate_column_averages():
    # 读取markdown文件并解析表格
    file_path = r'./Non_linear.md'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 找到表格数据行（跳过标题行和分隔符行）
    table_lines = []
    for line in lines:
        if line.strip().startswith('|') and 'Dataset' not in line and '---' not in line:
            table_lines.append(line.strip())
    
    # 解析表格数据
    data = []
    columns = []
    
    # 首先解析列名（从第一行获取）
    header_line = None
    for line in lines:
        if 'Dataset' in line and line.strip().startswith('|'):
            header_line = line.strip()
            break
    
    if header_line:
        columns = [col.strip() for col in header_line.split('|')[1:-1]]  # 去掉首尾空元素
    
    # 解析数据行
    for line in table_lines:
        row_data = [cell.strip() for cell in line.split('|')[1:-1]]  # 去掉首尾空元素
        data.append(row_data)
    
    # 创建DataFrame
    for i in range(len(data)):
        print(len(data[i]))
    print(len(columns))
    df = pd.DataFrame(data, columns=columns)
    
    # 将数值列转换为numeric类型（除了Dataset列）
    numeric_columns = df.columns[1:]  # 跳过Dataset列
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算每列的平均值
    averages = {}
    averages['Dataset'] = 'Average'
    
    for col in numeric_columns:
        avg_value = df[col].mean()
        averages[col] = round(avg_value, 2)
    
    # 创建包含平均值的新DataFrame
    avg_df = pd.DataFrame([averages])
    
    # 输出到CSV文件
    output_path = r'./Non_linear_averages.csv'
    avg_df.to_csv(output_path, index=False)
    
    print(f"列平均值已保存到: {output_path}")
    print("\n各列平均值:")
    for col, value in averages.items():
        if col != 'Dataset':
            print(f"{col}: {value}")
    
    return avg_df

# 运行脚本
if __name__ == "__main__":
    result = calculate_column_averages()