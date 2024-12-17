# pipelines.py

import json
import os

class NankaiSearchEnginePipeline:
    def __init__(self):
        # 设定存储目录
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def process_item(self, item, spider):
        # 保存抓取到的数据到 JSON 文件
        file_path = os.path.join(self.output_dir, f"{item['title']}.json")
        with open(file_path, 'w') as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=4)
        return item
