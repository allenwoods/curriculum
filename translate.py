import os
import requests
import base64
from pathlib import Path

# Configuration
API_KEY = 'dfba866f864c4af3be3b1542b9358747'
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Payload for the request
def gen_payload(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "请帮我将以下markdown内容翻译为中文。请保持格式完整，内容一致，请不要尝试精简其中的内容，也不要添加额外的解释。文本内容中的代码block和注释（即`<!--  -->`扩起的内容）也请不要翻译。内容取自Liveview专用的livemd格式，如果其中有属于格式设置相关的内容，也请保持原样。翻译的内容是一份Elixir学习文档，因此请注意不要翻译其中的一些专有名词，例如Elixir，Phoenix，Livebook等。"
        }
      ]
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": content}
        ]
    }
  ],
  "temperature": 0,
  "top_p": 0.95,
        "max_tokens": 16384
    }
    return payload

ENDPOINT = "https://allenwoods42.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview"

def translate(file_path, translated_file_path):
    payload = gen_payload(file_path)
    # Send request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    translated_content = response.json()['choices'][0]['message']['content']
    with open(translated_file_path, 'w') as file:
        file.write(translated_content)

def get_files(dir_name):
    files = Path(__file__).parent / f"{dir_name}_en"
    translated_files = Path(__file__).parent / f"{dir_name}"
    files = [file for file in files.iterdir() if file.suffix == ".livemd" and not file.name.startswith("_")]
    translate_files = [file for file in translated_files.iterdir() if file.suffix == ".livemd" and not file.name.startswith("_")]

    files_need_translate = {file: Path(str(file).replace(f"{dir_name}_en", dir_name)) for file in files if file not in translate_files}
    return files_need_translate

if __name__ == "__main__":
    files_need_translate = get_files("reading")
    print("Translating...")

    success_files = []
    failed_files = []
    for file, translated_file in files_need_translate.items():
        try:
          print(f"Translating {file}")
          translate(file, translated_file)
          success_files.append(file)
        except Exception as e:
          print(f"Failed to translate {file}: {e}")
          failed_files.append(file)
          continue
        
    print(f"Translated {len(success_files)} files:")
    print(success_files)
    print(f"Failed to translate {len(failed_files)} files:")
    print(failed_files)
    
