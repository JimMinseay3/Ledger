import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# 假设 extract_transaction_details 函数在 pdf_parser.py 中
from pdf_parser import extract_transaction_details

class PDFExtractorApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF信息提取工具")
        master.geometry("1000x700") # 增加窗口宽度以容纳新列
        master.minsize(1000, 700)  # 更新最小尺寸

        # 创建菜单栏
        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)

        self.menubar.add_command(label="选择PDF文件", command=self.select_pdf_files)
        self.menubar.add_command(label="退出", command=master.quit)

        # 创建主框架
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧框架：文件选择和预览
        self.left_frame = ttk.LabelFrame(self.main_frame, text="文件选择与预览", padding="10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)

        self.file_list_frame = ttk.Frame(self.left_frame)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(self.file_list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_list_scrollbar = ttk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.file_list_scrollbar.set)

        # 右侧框架：结果显示
        self.right_frame = ttk.LabelFrame(self.main_frame, text="提取结果", padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        # 添加搜索框
        self.search_frame = ttk.Frame(self.right_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.search_frame, text="搜索标的: ").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_var.trace_add("write", self.on_search)

        # 创建结果区域框架，用于更好地管理Treeview和滚动条
        self.result_area_frame = ttk.Frame(self.right_frame)
        self.result_area_frame.pack(fill=tk.BOTH, expand=True)

        # 更新Treeview，添加新列
        self.result_tree = ttk.Treeview(self.result_area_frame, columns=("Shares", "Valuation", "InitialPrice", "Premium"), show="headings", height=20)
        self.result_tree.heading("Shares", text="标的 (Shares)")
        self.result_tree.heading("Valuation", text="估值 (Valuation)")
        self.result_tree.heading("InitialPrice", text="初始价格 (Initial Price)")
        self.result_tree.heading("Premium", text="期权费率 (Premium(%))")
        self.result_tree.column("Shares", width=150, anchor=tk.W)
        self.result_tree.column("Valuation", width=150, anchor=tk.W)
        self.result_tree.column("InitialPrice", width=150, anchor=tk.W)
        self.result_tree.column("Premium", width=150, anchor=tk.W)
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.result_scrollbar = ttk.Scrollbar(self.result_area_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.config(yscrollcommand=self.result_scrollbar.set)

        # 存储所有数据用于搜索
        self.all_data = []

    def on_search(self, *args):
        search_text = self.search_var.get().lower()
        # 清空当前显示的结果
        self.result_tree.delete(*self.result_tree.get_children())

        # 如果搜索框为空，则显示所有数据
        if not search_text:
            for item in self.all_data:
                self.result_tree.insert("", tk.END, values=item)
            return

        # 根据搜索文本过滤结果
        for item in self.all_data:
            shares = item[0].lower()
            if search_text in shares:
                self.result_tree.insert("", tk.END, values=item)

    def select_pdf_files(self):
        file_paths = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_paths:
            self.file_listbox.delete(0, tk.END)  # 清空列表
            for path in file_paths:
                self.file_listbox.insert(tk.END, path)
            self.process_selected_files() # 自动处理文件

    def process_selected_files(self):
        self.result_tree.delete(*self.result_tree.get_children())  # 清空结果
        self.all_data = []  # 清空存储的所有数据
        # 处理所有已加载的文件
        all_file_paths = [self.file_listbox.get(i) for i in range(self.file_listbox.size())]
        if not all_file_paths:
            messagebox.showinfo("提示", "请先选择要处理的PDF文件！")
            return

        for file_path in all_file_paths:
            extracted_data = extract_transaction_details(file_path)

            if extracted_data:
                shares = extracted_data.get('Shares', 'N/A')
                valuation = extracted_data.get('Valuation', 'N/A')
                initial_price = extracted_data.get('Initial Price', 'N/A')
                premium = extracted_data.get('Premium(%)', 'N/A')

                # 格式化输出
                formatted_shares = shares.replace('.SH', '.SH\t') if '.SH' in shares else shares.replace('.SZ', '.SZ\t') if '.SZ' in shares else shares
                formatted_valuation = valuation.replace('CNY', 'CNY\t') if 'CNY' in valuation else valuation
                formatted_initial_price = initial_price.replace('CNY', 'CNY\t') if 'CNY' in initial_price else initial_price
                formatted_premium = premium.replace('%', '%\t') if '%' in premium else premium

                # 存储数据用于搜索
                data_item = (formatted_shares, formatted_valuation, formatted_initial_price, formatted_premium)
                self.all_data.append(data_item)
                self.result_tree.insert("", tk.END, values=data_item)
                self.master.update_idletasks()
                self.master.update()
            else:
                data_item = (f"无法提取 ({file_path.split('/')[-1]})", "无法提取", "无法提取", "无法提取")
                self.all_data.append(data_item)
                self.result_tree.insert("", tk.END, values=data_item)
                self.master.update_idletasks()
                self.master.update()