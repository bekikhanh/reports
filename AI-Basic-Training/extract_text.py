import json
from bs4 import BeautifulSoup
import re

with open('AI-Basics-for-bekiers_jp.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

text_nodes = []
# Extract text that looks like Vietnamese/content
for element in soup.find_all(string=True):
    parent = element.parent.name
    if parent not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        text = element.strip()
        if text and len(text) > 1 and re.search(r'[a-zA-ZáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]', text):
            text_nodes.append(text)

with open('text_to_translate.json', 'w', encoding='utf-8') as f:
    json.dump(text_nodes, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(text_nodes)} text nodes.")
