import time
from io import BufferedReader, TextIOWrapper
from openai import OpenAI
from openai.resources.beta.assistants import Assistant, SyncCursorPage
from openai.types import FileDeleted
from openai.types.beta import VectorStore, VectorStoreDeleted
from openai.types.beta.assistant_deleted import AssistantDeleted
from openai.types.beta.threads.message import Message
from openai.pagination import SyncPage
from openai.types.file_object import FileObject
from returns.result import Result, Success, Failure
from Assistant.Model.Constant import OpenApiTool
from Assistant.Model.ChattingEventHandler import ChattingEventHandler

# 自定義的GPT小助手class
class CustomAssistant:

    def __init__(self, api_key: str, file_folder_path: str, download_folder_path: str):
        """
        初始化助手

        參數:
            api_key: OpenAI的API-Key
            file_folder_path: 要上傳的檔案資料夾路徑
            download_folder_path: 要下載檔案的資料夾路徑
        """
        self.client = OpenAI(api_key=api_key)
        self.file_folder_path = file_folder_path
        self.download_folder_path = download_folder_path
        self.assistant = None
        self.thread = None
        self.assistant_id = None

    def create(self, name: str, instructions: str, model: str = "gpt-4o") -> str:
        """
        建立助手

        參數:
            name: 助手名稱
            instructions: 助手描述
            model: GPT模型名稱
        回傳:
            str: 助手Id
        """
        self.assistant = self.client.beta.assistants.create(name=name, instructions=instructions, model=model)
        self.assistant_id = self.assistant.id
        self.thread = self.client.beta.threads.create()

        return self.assistant.id
    
    def items(self, order: str = "desc") -> SyncCursorPage[Assistant]:
        """
        取得建立好的助手們

        參數:
            order: 照建立的順序排序
        回傳:
            SyncCursorPage[Assistant]
        """
        return self.client.beta.assistants.list(order=order)
    
    def upload_file_items(self) -> SyncPage[FileObject]:
        """
        取得上傳好的檔案們

        參數:
            order: 照建立的順序排序
        回傳:
            SyncPage[FileObject]
        """
        return self.client.files.list()
    
    def vector_store_items(self, order: str = "desc") -> SyncCursorPage[VectorStore]:
        """
        取得上傳傳好的向量資料們

        參數:
            order: 照建立的順序排序
        回傳:
            SyncCursorPage[VectorStore]
        """
        return self.client.beta.vector_stores.list(order=order)
    
    def remove_by_id(self, assistant_id: str) -> AssistantDeleted:
        """
        刪除該Id的助手

        參數:
            assistant_id: 助手Id
        回傳:
            AssistantDeleted
        """
        return self.client.beta.assistants.delete(assistant_id=assistant_id)

    def remove_by_name(self, assistant_name: str, delay_timeTime: float = 1.0) -> int:
        """
        刪除該名稱的助手們

        參數:
            assistant_name: 助手名稱
            delay_timeTime: 延遲時間
        回傳:
            int: 被刪除同名稱助手的數量
        """
        removeCount = 0
        assistants = self.find_by_name(assistant_name)

        for assistant in assistants:
            time.sleep(delay_timeTime)
            info = self.remove_by_id(assistant.id)
            if (info.deleted): removeCount += 1

        return removeCount
    
    def remove_vector_store_by_id(self, id: str) -> VectorStoreDeleted:
        """
        刪除該Id的VectorStore

        參數:
            vector_store_id: VectorStoreId
        回傳:
            VectorStoreDeleted
        """
        return self.client.beta.vector_stores.delete(id)
    
    def remove_vector_stores_by_name(self, name: str, delay_timeTime: float = 1.0) -> int:
        """
        刪除該名稱的VectorStore們

        參數:
            name: str
            delay_timeTime: 延遲時間
        回傳:
            int: 被刪除同名稱VectorStore的數量
        """
        removeCount = 0
        stores = self.find_vector_stores_by_name(name)

        for store in stores:
            time.sleep(delay_timeTime)
            info = self.remove_vector_store_by_id(store.id)
            if (info.deleted): removeCount += 1
        
        return removeCount
    
    def remove_upload_file_by_id(self, id: str) -> FileDeleted:
        """
        刪除該File_Id的檔案

        參數:
            id: File_Id
        回傳:
            FileDeleted
        """
        return self.client.files.delete(id)

    def remove_upload_files_by_name(self, name: str, delay_timeTime: float = 1.0) -> int:
        """
        刪除該名稱的檔案們

        參數:
            name: str
            delay_timeTime: 延遲時間
        回傳:
            int: 被刪除同名稱的檔案數量
        """
        removeCount = 0
        files = self.find_upload_files_by_name(name)

        for file in files:
            time.sleep(delay_timeTime)
            info = self.remove_upload_file_by_id(file.id)
            if (info.deleted): removeCount += 1

        return removeCount

    def find_by_id(self, assistant_id: str) -> Result[Assistant, Exception]:
        """
        使用「助手Id」找出該建立好的助手

        參數:
            assistant_id: 助手Id
        回傳:
            Result[Assistant, Exception]
        """
        try:
            assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
            return Success(assistant)
        except Exception as error:
            return Failure(error)

    def find_by_name(self, assistant_name: str) -> list[Assistant]:
        """
        使用「助手名稱」找出該建立好的助手們

        參數:
            assistant_name: 助手名稱
        回傳:
            list[Assistant]: 同名的助手們
        """
        assistants: list[Assistant] = []
        _assistants = list(self.items())

        for _assistant in _assistants:
            if (_assistant.name == assistant_name): assistants.append(_assistant)
        
        return assistants
    
    def find_upload_files_by_name(self, name:str) -> list[FileObject]:
        """
        使用「檔案名稱」找出該建立好的檔案們

        參數:
            name: Store名稱
        回傳:
            list[FileObject]: 同名的檔案們
        """
        files: list[FileObject] = []
        items = self.upload_file_items()
        
        for file in items.data:
            if file.filename != name: continue
            files.append(file)

        return files

    def find_vector_stores_by_name(self, name:str) -> list[VectorStore]:
        """
        使用「Vector-Store名稱」找出該建立好的Vector-Store們

        參數:
            name: Store名稱
        回傳:
            list[VectorStore]: 同名的VectorStore們
        """
        stores: list[VectorStore] = []
        vector_stores = self.vector_store_items()

        for vector_store in vector_stores.data:
            if vector_store.name != name: continue
            stores.append(vector_store)

        return stores

    def use_by_id(self, assistant_id: str) -> Result[str, Exception]:
        """
        利用「助手id」來使用助手

        參數:
            assistant_id: 助手id
        回傳:
            Result[<助手名稱>, Exception]
        """
        try:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
            self.assistant_id = self.assistant.id
            self.thread = self.client.beta.threads.create()

            return Success(self.assistant.name)
        
        except Exception as error:
            return Failure(error)
    
    def use_by_name(self, assistant_name: str) -> Result[str, Exception]:
        """
        利用「助手名稱」來使用找到的第一個助手

        參數:
            assistant_name: 助手名稱
        回傳:
            Result[<助手Id>, Exception]
        """
        assistants = self.find_by_name(assistant_name)
        
        if not assistants: return Failure(ValueError("找不到助手…"))
        return self.use_by_id(assistants[0].id)

    def update(self, parameters: dict) -> Result[str, Exception]:
        """
        更新助手資料

        參數:
            parameters: 要更新的相關參數
        回傳:
            Result[<助手Id>, Exception]
        """

        if not parameters: return Failure("沒有任何參數…")

        try:
            assistant = self.client.beta.assistants.update(
                assistant_id = self.assistant_id,
                **parameters
            )
            return assistant.id
        
        except Exception as error:
            return Failure(error)

    def update_information(self, name: str | None, instructions: str | None, model: str | None) -> Result[str, Exception]:
        """
        更新助手的基本資料

        參數:
            name: 助手名稱
            instructions: 助手敘述
            model: 使用模型
        回傳:
            Result[<助手Id>, Exception]
        """
        parameters = {}

        if (name != None and name.strip() != None): parameters["name"] = name
        if (instructions != None and instructions.strip() != None): parameters["instructions"] = instructions
        if (model != None and model.strip() != None): parameters["model"] = model

        return self.update(parameters)
    
    def update_tools(self, tools: list[OpenApiTool]) -> Result[str, Exception]:
        """
        開關助手的功能 (File Search / Code Interpreter)

        參數:
            tools: list[OpenApiTool]
        回傳:
            Result[<助手Id>, Exception]
        """
        types = []
        parameters = {}
        
        for tool in tools: 
            type = {}
            type["type"] = tool.value
            types.append(type)
        
        parameters["tools"] = types

        return self.update(parameters)

    def upload_file_for_file_search(self, filename: str) -> Result[dict, Exception]:
        """
        上傳純文字說明檔 for File Search功能 (.txt / ...)

        參數:
            filename: 檔案名稱
        回傳:
            Result[<上傳檔案的Id資訊>, Exception]
        """
        result = self.upload_vector_store_file(filename)

        match result:
            case Failure(error): return Failure(error)
            case Success(vector_store_id):
                try:
                    self.client.beta.assistants.update(
                        assistant_id = self.assistant_id,
                        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
                    )
                    return Success({ vector_store_id: filename })
                except Exception as error:
                    return Failure(error)

    def upload_file_for_code_interpreter(self, filename: str) -> Result[dict, Exception]:
        """
        上傳要傳成向量的資料檔 for Code Interpreter功能 ("c", "cpp", "css", "csv", "doc", "docx", "gif", "go", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", "php", "pkl", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip")

        參數:
            filename: 檔案名稱
        回傳:
            Result[<上傳檔案的Id資訊>, Exception]
        """
        result = self.upload_code_interpreter_file(filename)

        match result:
            case Failure(error): return Failure(error)
            case Success(file_id):
                try:
                    self.client.beta.assistants.update(
                        assistant_id = self.assistant_id,
                        tool_resources={"code_interpreter": {"file_ids": [file_id]}},
                    )
                    return Success({ file_id: filename })
                except Exception as error:
                    return Failure(error)

    def upload_files_for_code_interpreter(self, filenames: list[str]) -> Result[dict, Exception]:
        """
        上傳要傳成向量的資料檔們 for Code Interpreter功能 (.txt / .csv / .xlsx / ...)

        參數:
            filenames: 檔案們的名稱
        回傳:
            Result[<上傳檔案們的Id資訊>, Exception]
        """
        upload_files_dict = {}

        for filename in filenames:
            result = self.upload_code_interpreter_file(filename)
            match result:
                case Failure(error): break
                case Success(file_id): upload_files_dict[file_id] = filename

        try:
            file_ids = [key for key in upload_files_dict.keys()]

            self.client.beta.assistants.update(
                assistant_id = self.assistant_id,
                tool_resources={"code_interpreter": {"file_ids": file_ids}},
            )
            return Success(upload_files_dict)

        except Exception as error:
            return Failure(error)

    def upload_vector_store_file(self, filename: str):
        """
        將檔案上傳到知識庫 for File Search，然後取得VECTOR_STORE_ID

        參數:
            filename: 檔案名稱
        回傳:
            Result[<VECTOR_STORE_ID>, Exception]
        """
        file_path = f"{self.file_folder_path}{filename}"
        result = self.__open_file__(file_path)

        match result:
            case Failure(error): return Failure(error)
            case Success(file):
                try:
                    vector_store = self.client.beta.vector_stores.create(name=filename)
                    response = self.client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=[file])
                    if response.status == "completed": return Success(vector_store.id)
                except Exception as error:
                    return Failure(error)

    def upload_code_interpreter_file(self, filename: str) -> Result[str, Exception]:
        """
        將檔案上傳到知識庫 for Code Interpreter，然後取得FILE_ID

        參數:
            filename: 檔案名稱
        回傳:
            Result[<FILE_ID>, Exception]
        """
        file_path = f"{self.file_folder_path}/{filename}"
        result = self.__open_file__(file_path)

        match result:
            case Failure(error): return Failure(error)
            case Success(file):
                try:
                    upload_file = self.client.files.create(file=file, purpose="assistants")
                    return Success(upload_file.id)
                except Exception as error:
                    return Failure(error)

    def download_file(self, file_id: str) -> Result[bytes, Exception]:
        """
        檔案下載 (Purpose = assistants_output)

        參數:
            file_id: str
        回傳:
            Result[<二進制檔案>, Exception]
        """
        try:
            response = self.client.files.with_raw_response.content(file_id)
            if (response.status_code != 200): return Failure(f"下載失敗 (code={response.status_code})")
            return Success(response.content)
        except Exception as error:
            return Failure(error)

    def save_file(self, file_id: str, extension: str) -> Result[str, Exception]:
        """
        儲存下載的檔案 (Purpose = assistants_output)

        參數:
            file_id: str
            extension: 要存的檔案副檔名 (jpg / png / csv)
        回傳:
            Result[<檔案存檔路徑>, Exception]
        """
        file_path = f"{self.download_folder_path}{file_id}.{extension}"

        result = self.download_file(file_id)
        match result:
            case Failure(error): return error
            case Success(bytes): 
                self.__write_file__(bytes, file_path)
                return file_path

    def vector_store_id_exists(self, vector_store_id: str) -> bool:
        """
        測試VectorStoreId是否存在 / 已建立

        參數:
            vector_store_id: str
        回傳:
            bool
        """
        stores = self.vector_store_items()
        store_exists = any(store.id == vector_store_id for store in stores)

        return store_exists

    def chat(self, content: str, delay_timeTime: float = 1.0) -> Result[str, Exception]:
        """
        跟已建立好的「助手」詢問 / 對話

        參數:
            content: 對話文字內容
            delay_timeTime: 延遲時間
        回傳:
            Result[str, Exception]
        """
        try:
            if not content.strip(): return Failure(ValueError("不得輸入空白字串…"))

            self.__input_content__(content)
            run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant_id)
            
            while run.status != "completed":
                time.sleep(delay_timeTime)
                run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
            
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            text = messages.data[0].content[0].text.value

            if not text: return Failure(ValueError("沒有回應文字…"))
            return Success(str(text))

        except Exception as error:
            return Failure(error)

    def chatting(self, content: str, onTextDeltaBlock: lambda value: str, onCodeInterpreterInputBlock: lambda input: str):
        """
        跟已建立好的「助手」詢問 / 對話 (及時串流)

        參數:
            content: 對話文字內容
            onTextDeltaBlock: 回答的文字訊息
            onCodeInterpreterInputBlock: 跟程式碼有關的部分 (GPT的想法實作)
        """
        self.__input_content__(content)
        handler = ChattingEventHandler(onTextDeltaBlock, onCodeInterpreterInputBlock)

        with self.client.beta.threads.runs.stream(thread_id=self.thread.id, assistant_id=self.assistant.id, instructions=self.assistant.instructions, event_handler=handler) as stream:

            for stream_event in stream:
                try:
                    contentDelta = stream_event.data.delta.content[0]
                    value = contentDelta.text.value
                    if stream_event.event == "thread.message.delta": yield f'data: {value}\n\n'
                except Exception as error:
                    yield f'error: {error}\n\n'

    def __input_content__(self, content: str, role: str = "user") -> Message:
        """
        輸入要問的訊息

        參數:
            content: 對話文字內容
        """
        return self.client.beta.threads.messages.create(thread_id=self.thread.id, role=role, content=content)

    def __open_file__(self, file_path: TextIOWrapper, mode: str = "rb") -> Result[BufferedReader, Exception]:
        """
        開啟檔案

        參數:
            file_path: 檔案路徑
            mode: 開檔模式
        """
        try:
            file = open(file_path, mode)
            return Success(file)
        except Exception as error:
            return Failure(error)

    def __write_file__(self, bytes: bytes, file_path: TextIOWrapper) -> Result[int, Exception]:
        """
        寫入檔案 (二進制)

        參數:
            bytes: 二進制檔案
            file_path: 檔案路徑
            mode: 開檔模式
        回傳:
            Result[<寫入的檔案大小>, Exception]
        """
        result = self.__open_file__(file_path, "wb")

        match result:
            case Failure(error): return Failure(error)
            case Success(file): return Success(file.write(bytes))