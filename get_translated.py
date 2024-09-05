from pathlib import Path
import json

if __name__ == "__main__":
    sucess_count = 0
    fail_count = 0
    with open("translated.jsonl", "r") as f:
        for ix, line in enumerate(f):
            data = json.loads(line)
            try:
                ids = data['custom_id'].split("-")
                task_id = ids[0]
                dir_name = ids[1]
                file_name = data['custom_id'][len(task_id) + len(dir_name) + 2:]
            except ValueError as e:
                print(f"Skipping {ix} file: {data['custom_id']} due to {e}")
                fail_count += 1
                continue
            contents = data['response']['body']['choices'][0]['message']['content']

            # Check if the contents are valid
            assert contents is not None
            assert contents[-6:] == "</div>"

            print(f"Writing {ix} file: {dir_name}/{file_name}.livemd...")
            with open(f"{dir_name}/{file_name}.livemd", "w") as f:
                f.write(contents)
            sucess_count += 1
    print(f"Success: {sucess_count}, Fail: {fail_count}")