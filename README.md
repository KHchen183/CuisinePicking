# 美食挑選器  
歡迎查閱我的第一支小作品，Python 版本為 3.9.7。  
附打包執行檔，下載頁面：[Download](https://github.com/KHchen183/CuisinePicking/releases/tag/v0.1)  
(提醒：內含 exe 檔案，可能被瀏覽器誤判為惡意實體，但請安心使用)

# 前言
民以食為天，餐點想半天。為了解決"吃"的煩惱，製作了此美食挑選器，程式中加入多項功能(如：口袋名單資料庫、網路搜尋美食資訊、隨機挑選美食等)，並建立圖形化介面(GUI)，提升互動性。  

# 功能與操作  
* 圖形化介面(GUI)：  
  利用 Python 內建模組 Tkinter 製作。  
  <p align="left">
    <img width="800" src="https://github.com/KHchen183/CuisinePicking/blob/master/_PreviewPictures/Whole%20Win.png?raw=true">
  </p>

* 口袋名單資料庫：  
  程式本身以 Excel 作為資料庫存取所有店家資訊，可於視窗中編輯、新增或移除，也可至後台 Excel 檔案進行資料處裡。  
  1.編輯、移除功能  
  <img width="480" src="https://github.com/KHchen183/CuisinePicking/blob/master/_PreviewPictures/Edit%20and%20Delete.gif?raw=true">  
  2.新增功能  
  <img width="480" src="https://github.com/KHchen183/CuisinePicking/blob/master/_PreviewPictures/Add.gif?raw=true">  

* 網路搜尋美食資訊：  
  利用網路爬蟲抓取美食網站—[愛食記](https://ifoodie.tw/)的美食資訊，且可以將喜愛的店家資訊儲存至口袋名單。  
  1.搜尋美食資訊  
  <img width="800" src="https://github.com/KHchen183/CuisinePicking/blob/master/_PreviewPictures/Search.gif?raw=true">  
  2.加入至清單中(單一新增、全部新增)    
  <img width="800" src="https://github.com/KHchen183/CuisinePicking/blob/master/_PreviewPictures/Add%20to%20database.gif?raw=true">  
  
* 隨機挑選美食：  
  建立篩條件(如：種類、價位、縣市地區等)，縮小挑選範圍，達到符合實際情況的可行性。  

# 技巧想法
* 多執行緒：  
  Tkinter 製作的視窗無法同時多功處理，在爬取網頁資料時，視窗無法進行其他操作，為此加開一條執行緒提供爬蟲搜尋資料，同時可以在視窗中預覽已經抓取到的部分資訊。  
  ```python
  import threading as thd
  thread_1 = thd.Thread(target = function, name = "T1")
  thread_1.start()
  thread_1.join()
  ```  
* 多核心：  
  爬蟲抓取多筆店家資訊的網頁，利用 CPU 多核心運行可以大幅縮短獲取資料的時間。  
  ```python
  pool = mp.Pool()
  multi_res = pool.map(function, inputs)
  pool.close()
  pool.join()
  ```
