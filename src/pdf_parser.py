import pdfplumber

def extract_transaction_details(pdf_path):
    """
    从交易确认书PDF中提取股票、估值、初始价格和溢价百分比信息。
    支持两种不同格式的结算确认书。

    参数:
        pdf_path (str): PDF文件的路径。

    返回:
        dict: 包含提取出的信息的字典，如果未找到则返回 None。
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 假设表格在第一页，如果表格可能在其他页，你需要遍历所有页面。
            page = pdf.pages[0]
            
            # 提取页面上的所有表格
            tables = page.extract_tables()

            if tables:
                table_data = tables[0]
                
                shares_value = None
                valuation_value = None
                settlement_income_value = None
                initial_price_value = None
                premium_percent_value = None
                premium_value = None
                
                # 遍历表格中的每一行
                for row in table_data:
                    # 检查行的第一个单元格是否为目标字段
                    if row[0] == "Shares:":
                        shares_value = row[1]
                    elif row[0] == "Valuation:":
                        valuation_value = row[1]
                    elif row[0] == "Settlement Income:":
                        settlement_income_value = row[1]
                    elif row[0] == "Initial Price:":
                        initial_price_value = row[1]
                    elif row[0] == "Premium (%):":
                        premium_percent_value = row[1]
                    elif row[0] == "Premium(%):":
                        premium_percent_value = row[1]
                    elif row[0] == "Premium:":
                        premium_value = row[1]
                
                # 确定最终的估值值：
                # 1. 如果有Settlement Income，则优先使用
                # 2. 否则如果Valuation不为空且不为"None"，则使用Valuation
                # 3. 否则如果Premium不为空，则使用Premium
                final_valuation = "N/A"
                if settlement_income_value:
                    final_valuation = settlement_income_value
                elif valuation_value and valuation_value != "None":
                    final_valuation = valuation_value
                elif premium_value:
                    final_valuation = premium_value
                
                # 如果至少找到了Shares，就返回结果
                if shares_value:
                    result = {
                        "Shares": shares_value,
                        "Valuation": final_valuation
                    }
                    
                    # 如果找到了其他字段，也添加到结果中
                    if initial_price_value:
                        result["Initial Price"] = initial_price_value
                    if premium_percent_value:
                        result["Premium(%)"] = premium_percent_value
                    
                    return result
    
    except Exception as e:
        print(f"发生错误: {e}")
        return None