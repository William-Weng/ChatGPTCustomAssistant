# [說明](https://platform.openai.com/)

## 使用OpenAI產生自訂的小助手
![Example](Example.webp)

## 安裝套件 - Python 3.13.0
```python
python3 -m venv .venv
pip3 install openai returns
```

## CustomAssistant
|函式名稱|功能|
|-|-|
|\_\_init\_\_(api_key:file_folder_path:download_folder_path:)|初始化助手|
|create(name:instructions:model:)|建立助手|
|items(order:)|取得建立好的助手們|
|upload_file_items()|取得上傳好的檔案們|
|vector_store_items(order:)|取得上傳傳好的向量資料們|
|remove_by_id(assistant_id:)|刪除該Id的助手|
|remove_by_name(assistant_name:delay_time:)|刪除該名稱的助手們|
|remove_vector_store_by_id(id:)|刪除該Id的VectorStore|
|remove_vector_stores_by_name(name:delay_time:)|刪除該名稱的VectorStore們|
|remove_upload_file_by_id(id:)|刪除該File_Id的檔案|
|remove_upload_files_by_name(name:delay_time:)|刪除該名稱的檔案們|
|find_by_id(assistant_id:)|使用「助手Id」找出該建立好的助手|
|find_by_name(assistant_name:)|使用「助手名稱」找出該建立好的助手們|
|find_upload_files_by_name(name:)|使用「檔案名稱」找出該建立好的檔案們|
|find_vector_stores_by_name(name:)|使用「Vector-Store名稱」找出該建立好的Vector-Store們|
|use_by_id(assistant_id:)|利用「助手id」來使用助手|
|use_by_name(assistant_name:)|利用「助手名稱」來使用找到的第一個助手|
|update(parameters:)|更新助手資料|
|update_information(name:instructions:model:)|更新助手的基本資料|
|update_tools(tools:)|更新助手的功能 (File Search / Code Interpreter)|
|upload_file_for_file_search(filename:)|上傳純文字說明檔 for File Search功能 (.txt / ...)|
|upload_file_for_code_interpreter(filename:)|上傳要傳成向量的資料檔 for Code Interpreter功能 (.txt / .csv / .xlsx / ...)|
|upload_files_for_code_interpreter(filenames:)|上傳要傳成向量的資料檔們 for Code Interpreter功能 (.txt / .csv / .xlsx / ...)|
|upload_vector_store_file(filename:)|將檔案上傳到知識庫 for File Search，然後取得VECTOR_STORE_ID|
|upload_code_interpreter_file(filename:)|將檔案上傳到知識庫 for Code Interpreter，然後取得FILE_ID|
|download_file(file_id:)|檔案下載 (Purpose = assistants_output)|
|save_file(file_id:extension:)|儲存下載的檔案 (Purpose = assistants_output)|
|vector_store_id_exists(vector_store_id:)|測試VectorStoreId是否存在 / 已建立|
|chat(content:)|跟已建立好的「助手」詢問 / 對話|
|chatting(content:onTextDeltaBlock:onCodeInterpreterInputBlock:)|跟已建立好的「助手」詢問 / 對話 (及時串流)|
