# Using Azure OpenAI API to translate markdown files in batch
# See https://learn.microsoft.com/zh-cn/azure/ai-services/openai/how-to/batch?tabs=standard-input&pivots=programming-language-ai-studio

import requests
from pathlib import Path
import json


# Payload for the request
def gen_payload(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    payload = {
  "messages": [
    {
      "role": "system",
      "content": "请帮我将以下markdown内容翻译为中文。请保持格式完整，内容一致，请不要尝试精简其中的内容，也不要添加额外的解释。文本内容中的代码block和注释（即`<!--  -->`扩起的内容）也请不要翻译。内容取自Liveview专用的livemd格式，如果其中有属于格式设置相关的内容，也请保持原样。翻译的内容是一份Elixir学习文档，因此请注意不要翻译其中的一些专有名词，例如Elixir，Phoenix，Livebook等。"
    },
    {
        "role": "user",
        "content": content # Note: Azure OpenAI API only support string type for content
    }
  ],
  "temperature": 0,
  "top_p": 0.95,
        "max_tokens": 16384
    }
    return payload


def get_files(dir_name):
    files = Path(__file__).parent / f"{dir_name}_en"
    files = [file for file in files.iterdir() if file.suffix == ".livemd" and not file.name.startswith("_") and not file.name.startswith("deprecated_")]
    
    translated_files = Path(__file__).parent / f"{dir_name}"
    translate_files = [file for file in translated_files.iterdir() if file.suffix == ".livemd" and not file.name.startswith("_") and not file.name.startswith("deprecated_")]

    files_need_translate = [file for file in files if file.name not in [file.name for file in translate_files]]
    files_need_translate = {file: Path(str(file).replace(f"{dir_name}_en", dir_name))for file in files_need_translate}
    return files_need_translate

if __name__ == "__main__":
    count = 0
    json_content = []
    for dir_name in ["reading", "exercises"]:
      files_need_translate = get_files(dir_name)
      print(f"Translating {len(files_need_translate)} files...")

      for ix, (file, translated_file) in enumerate(files_need_translate.items()):
            content = gen_payload(file)
            payload = {
            "custom_id": f"task{count}-{dir_name}-{file.name.replace('.livemd', '')}",
            "method": "POST",
            "url": "/chat/completions",
            "body": {
                "model": "gpt-4o-mini-batch",
                "messages": content["messages"],
                "temperature": 0,
                "top_p": 0.95,
                "max_tokens": 16384
                }
            }
            json_content.append(json.dumps(payload))
            count += 1
            
      with open(f"need_translate.jsonl", "w", encoding="utf-8") as f:
          f.writelines([item + "\n" for item in json_content])
      print(f"{count} files translated")
