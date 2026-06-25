# 元智大學智慧學生證掃描機 (YZU Smart Student ID Scanner)

這是一個基於 Python 與 OpenCV 開發的簡易即時物件偵測系統，作為電機系期末專題作品。本系統透過筆電視訊鏡頭，能即時掃描並鎖定「元智大學學生證」。

## 💡 專案亮點與解決方案
在開發初期，由於傳統的 Haar Cascade 形狀訓練模型容易受到塑膠卡片反光與複雜背景的干擾，導致辨識率不佳。
為了優化系統穩定度，本專案導入了以下兩項改良：
1. **設定 ROI (Region of Interest) 掃描區**：在畫面正中央繪製一個「黃色掃描框」，強制系統只對框內的畫面進行運算，100% 阻絕了背景（如海報、人臉）的干擾，同時大幅提升運算速度。
2. **鎖定證件大頭照特徵**：改為採用 OpenCV 官方強大的 `haarcascade_frontalface_default.xml` 模型，精準鎖定學生證上的「證件照」作為辨識依據，避開了卡片邊緣反光的問題。

## 📁 檔案結構
* `project.py`：即時掃描與影像處理的主程式。
* `haarcascade_frontalface_default.xml`：OpenCV 官方開源的臉部特徵分類器模型。

## 🛠️ 環境與安裝套件
本系統於 Windows 環境下開發，請確保您的電腦已安裝 Python (建議版本 3.8 以上)。

1. **安裝 OpenCV 影像處理套件：**
   請打開終端機 (Terminal) 或命令提示字元 (cmd)，輸入以下指令安裝所需套件：
   ```bash
   pip install opencv-python
2. **下載人臉開源圖像辨識檔案：**
   https://github.com/opencv/opencv/tree/master/data/haarcascades
3. **將下載好的`haarcascade_frontalface_default.xml`檔案放進程式的資料夾中**
