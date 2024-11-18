import time
from returns.result import Success, Failure
from Assistant.CustomAssistant import CustomAssistant

Api_Key = "<你猜猜>"
Assistant_Id = "<不告訴你>"
Assistant_Name = "一夜致富分析師 - William"
Instructions = "想要翻身致富、一夜暴富嗎？不用等待,馬上行動！只要加入我們的投資計劃,快速累積財富不是夢。專業團隊為您打造最佳投資組合,讓您輕鬆賺取高報酬。每月穩定收益,年化報酬率高達30%!過去一年已有上千人成功致富。立即諮詢,機會難得,早加入早獲利。快來成為下一位百萬富翁,實現財富自由夢想!讓財富自由不再是遙不可及的夢想。"

File_Folder_Path = "~/NoMoneyNoTalking"
Download_Folder_Path = "~/NoMoneyNoHoney"

def main():

    menuAssistant = CustomAssistant(Api_Key, File_Folder_Path, Download_Folder_Path)
    # result = menuAssistant.create(Assistant_Name, Instructions, "gpt-4o")
    result = menuAssistant.use_by_id(Assistant_Id)

    match result:
        case Failure(error): print(error)
        case Success(name): chat(menuAssistant, name)

def chat(assistant: CustomAssistant, name: str):

    print(f"開始跟<{name}>對話 (輸入 'quit' 結束)：")

    while True:

        user_input = input("You: ")
        if user_input.lower() == 'quit': break
        
        time.sleep(0.5)
        result = assistant.chat(user_input)
        match result:
            case Success(value): print(value)
            case Failure(error): print(error)

if __name__ == "__main__":
    main()
