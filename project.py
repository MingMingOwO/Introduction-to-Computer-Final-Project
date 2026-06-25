import cv2  # 載入 OpenCV 套件，這是用來處理影像的強大工具

# 1. 讀取官方寫好的人臉辨識大腦 (XML模型檔案)
# 因為自己訓練的形狀模型容易受反光影響，所以改用官方模型來抓「學生證上面的大頭照」！
# 注意：路徑絕對不能有中文，前面加 r 是為了告訴 Python 裡面的 \ 不要亂轉譯
cascade_model = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# 2. 打開筆電的視訊鏡頭 (0 代表預設的第一顆鏡頭)
cap = cv2.VideoCapture(0)

print("智慧學生證掃描機 啟動！按 'q' 關閉。")

# 3. 進入無窮迴圈，讓鏡頭不斷捕捉畫面，看起來就像影片一樣
while True:
    ret, frame = cap.read()  # ret 代表有沒有成功讀到畫面，frame 是拍到的那張照片
    if not ret:
        break  # 如果沒抓到畫面就跳出迴圈
        
    # 將彩色的照片變成黑白的（灰階），因為電腦處理黑白圖片的速度比較快
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # === 新增的絕招：設定一個特定掃描框 (ROI) ===
    # 為了避免官方模型太強，一直抓到背景的海報或我自己的臉，所以限定電腦只能看中間
    
    # 先取得現在鏡頭畫面的總高度跟總寬度
    height, width = frame.shape[:2]
    
    # 算一下螢幕正中間的座標，準備畫一個 寬300、高200 的掃描區
    x1 = int(width/2 - 150)
    y1 = int(height/2 - 100)
    x2 = int(width/2 + 150)
    y2 = int(height/2 + 100)
    
    # 在畫面上畫出這個黃色的掃描指示框，提醒使用者要把證件放在這裡
    # (0, 255, 255) 是黃色，最後的 2 是線條粗細
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(frame, "Please put YZU ID Card here", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # 重點來了！把「黃色掃描框」裡面的黑白畫面單獨剪下來
    # 這樣電腦就變成了井底之蛙，只會專心看這個小框框裡的東西
    scan_zone = gray[y1:y2, x1:x2]
    
    # 4. 開始偵測
    # 讓模型「只在剛剛剪下來的 scan_zone 裡面」找尋大頭照的特徵
    # minNeighbors=4 是一個適中的嚴格度參數+
    faces = cascade_model.detectMultiScale(scan_zone, scaleFactor=1.1, minNeighbors=4)
    
    # 5. 如果有找到大頭照，就把結果畫在螢幕上
    for (fx, fy, fw, fh) in faces:
        # 要特別注意！因為 fx, fy 是在「小框框」裡的相對座標
        # 我們必須把它加上黃色框框的起點 (x1, y1)，換算回整個大螢幕的真正位置
        real_x = x1 + fx
        real_y = y1 + fy
        
        # 畫出綠色的框框，代表成功抓到學生證上的大頭照了！
        cv2.rectangle(frame, (real_x, real_y), (real_x+fw, real_y+fh), (0, 255, 0), 2)
        
        # 標上我的學號，證明這是我的期末專題作品
        cv2.putText(frame, 'YZU 1120845 ID_Photo', (real_x, real_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    # 6. 把畫好所有框框的最終畫面，顯示在視窗上給我們看
    cv2.imshow('1120845 Smart ID Scanner', frame)
    
    # 7. 確保程式不會當機的關鍵！
    # 讓每一張畫面停留 1 毫秒，同時檢查我有沒有按下鍵盤的 'q' 鍵
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 8. 關閉程式時的收尾動作：把鏡頭還給電腦，並關掉所有跳出來的視窗
cap.release()
cv2.destroyAllWindows()