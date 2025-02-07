import os

def start_indexing(root_dir):
    """
    从给定的根目录开始索引文件。

    本函数遍历指定的根目录下的所有文件，对每个文件进行索引操作。
    索引操作在这里仅指打印文件的路径，但实际应用中可以包括更多逻辑，
    比如读取文件内容并建立索引等。

    参数:
    root_dir -- 根目录的路径，遍历将从这个目录开始。

    返回:
    indexed_files -- 返回索引的文件数量。
    """
    indexed_files = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # 这里可以添加更多的索引逻辑，比如读取文件内容等
            print(f"索引文件：{os.path.join(root, file)}")
            indexed_files += 1
    return indexed_files

def search_files(keyword):
    """
    在指定的根目录下搜索包含关键字的文件。

    通过递归遍历根目录中的所有文件，打开并检查文件内容是否包含给定的关键字。
    如果文件内容包含关键字，则将文件路径添加到结果列表中。

    参数:
    keyword (str): 要搜索的关键字。

    返回:
    list: 包含关键字的文件路径列表。
    """
    results = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                if keyword in content:
                    results.append(file_path)
    return results