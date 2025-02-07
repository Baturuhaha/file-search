import os
from PyPDF2 import PdfReader
from docx import Document
import sqlite3
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建数据库连接
conn = sqlite3.connect('document_index.db')
cursor = conn.cursor()

# 初始化表结构
cursor.execute('''CREATE TABLE IF NOT EXISTS documents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  file_path TEXT UNIQUE,
                  content TEXT)''')

conn.commit()

def index_documents(root_dir):
    """
    遍历指定根目录及其子目录，索引所有PDF和Word文档。
    """
    batch_size = 100  # 批量插入大小
    documents_to_insert = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.pdf'):
                try:
                    with open(file_path, 'rb') as f:
                        reader = PdfReader(f)
                        content = ''
                        for page in reader.pages:
                            content += page.extract_text()
                        documents_to_insert.append((file_path, content))
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {str(e)}")
            elif file.endswith('.docx'):
                try:
                    with open(file_path, 'rb') as f:
                        doc = Document(f)
                        content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                        documents_to_insert.append((file_path, content))
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {str(e)}")
            
            # 批量插入
            if len(documents_to_insert) >= batch_size:
                cursor.executemany('INSERT OR IGNORE INTO documents (file_path, content) VALUES (?, ?)', documents_to_insert)
                conn.commit()
                documents_to_insert.clear()
    
    # 插入剩余的文档
    if documents_to_insert:
        cursor.executemany('INSERT OR IGNORE INTO documents (file_path, content) VALUES (?, ?)', documents_to_insert)
        conn.commit()

def search_documents(query):
    """
    根据查询关键词搜索文档内容。
    """
    cursor.execute('SELECT file_path FROM documents WHERE content LIKE ?', ('%' + query + '%',))
    results = cursor.fetchall()
    return [row[0] for row in results]

if __name__ == '__main__':
    root_dir = input("请输入要索引的根目录路径：")
    index_documents(root_dir)
    
    print("\n文档索引完成！现在可以进行搜索。")
    
    while True:
        query = input("\nEnter your search keywords (输入'q'退出): ")
        if query.lower() == 'q':
            break
        results = search_documents(query)
        if results:
            print(f"找到 {len(results)} 个匹配的文档：")
            for path in results:
                print(path)
        else:
            print("没有找到匹配的文档。")
    conn.close()