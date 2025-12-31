from pdf_parser import extract_transaction_details

import tkinter as tk
from gui import PDFExtractorApp

def main():
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()