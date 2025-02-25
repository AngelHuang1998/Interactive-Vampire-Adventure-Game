import time  # 用於處理時間相關的功能，例如延遲執行
import sys   # 用於系統操作，例如程序退出、命令行參數等
import turtle # 用於繪製圖形和圖案
import os # 用於文件和目錄操作
import random # 用於隨機數的生成
import pygame  # 用於播放音樂和聲音效果
import threading  # 用於多執行緒執行，使得音效播放和主程序可同時進行
random.seed(time.time())  # 設定隨機數生成的種子，基於當前時間確保隨機性

t = 1.5  # 控制間隔的時間

def load_file_content(file_name):
    """
    檢查檔案是否存在並讀取內容。
    如果檔案不存在，則提示錯誤並結束程式。
    """
    if not os.path.exists(file_name):    # 檔案不存在  #os 模組提供 path.exists() 方法來確認指定的檔案或資料夾是否存在。
        print(f"Error: {file_name} is missing. Please add it to the program directory.")
        sys.exit()
    with open(file_name, "r", encoding="utf-8") as file:   #檔案存在
        return file.read()

def get_input(prompt):
    """
    如果用戶輸入為 "quit"，則退出程式。
    """
    user_input = input(prompt)
    if user_input.lower() == "quit":
        print("Exiting the story. Goodbye!")
        sys.exit()
    return user_input

def play_sound_effect(sound_name):
    """
    播放指定的音效檔案。
    如果音效檔案存在，則使用 pygame 模組播放。
    如果檔案缺失或發生錯誤，則輸出相應提示。
    """
    sound_files = {
        "poor": "poor.mp3",
        "rich": "rich.mp3"
    }

    if sound_name in sound_files and os.path.exists(sound_files[sound_name]):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_files[sound_name])  #載入音效檔案
            pygame.mixer.music.set_volume(1.0)  #設置音量
            pygame.mixer.music.play()   #播放音效

            # 設置播放的時長不超過10秒
            start_time = time.time()
            while pygame.mixer.music.get_busy():  
                if time.time() - start_time > 10:
                    break
                time.sleep(0.1)  # 讓程式每 0.1 秒檢查一次音樂是否還在播放，減少 CPU 資源消耗
        except Exception as e:    # try 內的任何一行發生錯誤，Python 會立刻進入 except 區塊，而不會讓程式崩潰
            print(f"Error playing sound {sound_files[sound_name]}: {e}")
    else:
        print(f"Error: {sound_files.get(sound_name, 'Unknown')} not found.")



def play_sound_effect(sound_name):
    """
    播放指定的音效檔案。
    如果音效檔案存在，則使用 pygame 模組播放。
    如果檔案缺失或發生錯誤，則輸出相應提示。
    """
    sound_files = {
        "poor": "poor.mp3",
        "rich": "rich.mp3"
    }

    # 檢查sound_name 是否在 sound_files 中，且對應的音效檔案是否存在
    if sound_name in sound_files and os.path.exists(sound_files[sound_name]):

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_files[sound_name])  #載入音效檔案
        
       
        #try 內的任何一行發生錯誤，Python 會立刻進入 except 區塊，而不會讓程式崩潰
        except pygame.error as e:     # pygame相關的錯誤
            print(f"Pygame error while loading {sound_files[sound_name]}: {e}")
        except FileNotFoundError:     #檔案遺失錯誤
            print(f"Error: {sound_files[sound_name]} not found.")
        except Exception as e:        #其他未預期的錯誤
            print(f"Unexpected error: {e}")


        # 只有當 try 沒有錯誤時，才執行這部分
        else:  
            pygame.mixer.music.set_volume(1.0)   #設置音量
            pygame.mixer.music.play()   #播放音效

            start_time = time.time()     
            while pygame.mixer.music.get_busy():   # 設置播放的時長不超過10秒
                if time.time() - start_time > 10:
                    break
                time.sleep(0.1)   # 讓程式每 0.1 秒檢查一次音樂是否還在播放，減少 CPU 資源消耗


    else:   # 如果 sound_name 不在 sound_files中，或是對應的音效檔案不存在
        print(f"Error: {sound_files.get(sound_name, 'Unknown')} not found.")



def draw_diamond(layers):
    """
    繪製鑽石外部輪廓: 倒三角形的鑽石。
    """
    turtle.speed(0)  # 設置繪圖速度
    top_y = 220  # 鑽石頂部的 y 座標
    turtle.penup()
    turtle.goto(-10 * (layers - 1), top_y)  # 移動到頂部起點
    turtle.pendown()

    for layer in range(layers, 0, -1):  # 從最上層繪製到最底層
        start_x = -10 * (layer - 1)  # 當前層的起始 x 座標
        start_y = top_y - (layers - layer) * 20  # 當前層的起始 y 座標
        turtle.penup()
        turtle.goto(start_x, start_y)
        turtle.pendown()

        for _ in range(layer):  # 繪製當前層的倒三角形
            draw_inverted_triangle(20)  # 倒三角形邊長為 20
            turtle.penup()
            turtle.forward(20)  # 移動到下一個倒三角形的位置
            turtle.pendown()

    return start_y - 20  # 返回鑽石底部的 y 座標

def draw_inverted_triangle(size):
    """
    繪製鑽石內部: 鑽石內部是由多個倒三角形組成。
    參數 size: 三角形的邊長。
    """
    turtle.fillcolor("blue")  #鑽石顏色
    turtle.begin_fill()
    for _ in range(3):
        turtle.forward(size)
        turtle.right(120)  # 轉角方向確保是倒三角形
    turtle.end_fill()

def draw_diamond_with_ring(layers):
    """
    繪製鑽戒的底部圓環。
    參數 layers: 鑽石的層數。
    """
    # y座標的起始位置設定在鑽石底部
    diamond_bottom_y = draw_diamond(layers)

    # 繪製圓環外圈
    ring_center_y = diamond_bottom_y - 95
    turtle.penup()
    turtle.goto(10, ring_center_y)
    turtle.pendown()
    turtle.fillcolor("gold")
    turtle.begin_fill()
    turtle.circle(50)  
    turtle.end_fill()

    # 繪製圓環的內部空心部分
    turtle.penup()
    turtle.goto(10, ring_center_y + 10)
    turtle.pendown()
    turtle.fillcolor("white")
    turtle.begin_fill()
    turtle.circle(40)  # 內圈
    turtle.end_fill()



def display_message(message, x, y, font_size=18):
    """
    使用 turtle 在畫布上顯示訊息。
    參數：
    - message: 要顯示的文字內容。
    - x, y: 文字顯示的位置。
    - font_size: 字體大小。
    """
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.hideturtle()
    turtle.write(message, align="center", font=("Arial", font_size, "bold"))


def play_sound_and_display_message(sound_name, message, x, y, font_size=18):
    """
    同時播放音效並顯示訊息。
    使用多執行緒處理音效播放，避免阻塞主程序。
    """
    sound_thread = threading.Thread(target=play_sound_effect, args=(sound_name,))
    sound_thread.start()  # 啟動 音效播放執行緒

    display_message(message, x, y, font_size)  # 顯示訊息由主執行緒執行
    sound_thread.join()  # 等待音效播放完成
    


def main():
    """
    主遊戲流程，包含故事線與互動邏輯。
    用戶透過選項與電腦進行互動，影響故事的進展。
    """
    print("Prompt: You can type \"quit\" to exit the program.")

    # 提示用戶按 Enter 繼續
    get_input("(press enter to start)\n")

    # 加載故事的開頭介紹
    intro = load_file_content("Intro_1.txt")
    print(intro)

    get_input("(press enter to start)\n")
    # 提示用戶是否想了解 Adam 的特殊身份
    ans1 = get_input("\"Adam actually has a special identity. Do you want to know?\"(yes/no)\n")

    if ans1 in "no":
        # 若用戶選擇不想知道，則加載相應的文本並顯示，之後等待一段時間
        identity_no = load_file_content("identity_No_2.txt")
        print(identity_no)
        time.sleep(t)

    # 顯示 Adam 作為吸血鬼的秘密身份背景
    print("""\"What people don't know is that Adam is actually a vampire, 
hiding among humans with great wealth.\"\n""")
    time.sleep(t)

    # 提示用戶按 Enter 繼續
    get_input("(press enter to continue)\n")

    # 顯示故事進一步發展，描述 Jenny 遇到意外的場景
    print("\"One night, after staying late at the school library, Jenny accidentally falls down the stairs\"\n")
    time.sleep(t)

    # 提問 Adam 是否想拯救 Jenny
    ans2 = get_input("\"Adam, do you want to save her? (yes/no)\n")
    time.sleep(t)

    while True:
        if ans2 in "yes":
            # 若選擇拯救，顯示相應的故事情節並暫停
            save_yes = load_file_content("Save or not_Yes_3.txt")
            print(save_yes)
            get_input("(press enter to continue)\n")
        else:
            # 若選擇不拯救，顯示不同的故事情節
            save_no = load_file_content("Save or not_No_4.txt")
            print(save_no)
            time.sleep(2.5)
            print(" ")

            # 提問是否想改變 Jenny 對自己的看法並追求她
            ans4 = get_input("\"Adam, do you want to change her perception of you and pursue her? (yes/no)\n")

            if ans4 in "yes":
                # 若選擇追求，返回上一個問題
                ans2 = "yes"
                print("(Yes, I want to save her)\n")
                continue
            else:
                # 若選擇放棄，故事結束
                print("The two will have no further interaction and become strangers.")
                print("(The story ends.)")
                break

        # 顯示 Jenny 的父親設置的困難條件
        print(" ")
        print("""However, Jenny's father is a very traditional man who could never accept the existence of a "non-human" being. 
The financial pressures on her family also make it hard for Jenny to pursue her own happiness.\n""")
        time.sleep(3)

        # 提問 Adam 是否願意接受條件
        ans3 = get_input("Father: \"Adam, if you want to pursue my daughter, are you willing to agree to one of three conditions?\" (yes/no)\n")
        choices = {
            "1": "(I will give up my chance at immortality and become an ordinary human.)",
            "2": "(I will sever all ties with my family)",
            "3": "(I will become a vegetarian from now on.)"
        }

        if ans3 in "yes":
            # 顯示接受條件的故事情節
            agree_yes = load_file_content("Agree Condition or not_Yes_5.txt")
            print(agree_yes)

            while True:
                # 提問選擇具體的條件，或讓父親幫助選擇
                ans5 = get_input("Please answer 1, 2, 3, or 4 (Father, please choose for me):\n")
                if ans5 in choices:
                    print(choices[ans5])
                    break
                elif ans5 == "4":
                    # 隨機選擇條件
                    random_choice = random.choice(list(choices.keys()))
                    print(choices[random_choice])
                    break
                else:
                    print("Invalid choice. Please try again.")

            time.sleep(t)
        else:
            # 顯示不接受條件的故事結尾
            agree_no = load_file_content("Agree Condition or not_No_6.txt")
            print(agree_no)
            break

        # 最終的鑽戒準備環節
        print("\nFather: Very well, you've earned the chance to propose to my daughter.\n")

        while True:
            # 問Adam要準備多大的鑽戒(幾層)
            layer = get_input("Adam, how many layers of diamond do you want to prepare for proposing?(At least 4 layers)\n")
            if layer.isdigit() and int(layer) >= 4:
                layer = int(layer)
                print("Diamond loading...\n")
                draw_diamond_with_ring(layer)  # 繪製鑽戒
                if layer >= 7:
                    # 層數足夠多，播放「富有」的音效並顯示相關訊息
                    play_sound_and_display_message(
                        "rich",
                        "Wow, this diamond is so big! Rich Boy!!\n Wish you two lived happily ever after.",
                        0,
                        -250,
                        18
                    )
                else:
                    # 層數較少，播放「貧窮」的音效並顯示相關訊息
                    play_sound_and_display_message(
                        "poor",
                        "It's too small. Are you poor?\n You may get divorced soon...",
                        0,
                        -250,
                        18
                    )
                turtle.done()
                sys.exit()  # 結束程式
            else:
                print("\nThat's too small!! Please input again!")

            

# 執行主程式
if __name__ == "__main__":
    main()
