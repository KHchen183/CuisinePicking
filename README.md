# 美食挑選器  
歡迎查閱我的小作品，Python 版本為 3.9.7。  
附打包執行檔，下載點：[Download](https://github.com/KHchen183/CuisinePicking/releases/tag/v0.1)  
(注意：內含 exe 檔案，可能被瀏覽器誤判為惡意實體，但請安心使用)

# 前言
民以食為天，餐點想半天。為此製作常見的食物選擇器，並加入多項額外功能（口袋名單資料庫、網路搜尋美食資訊、隨機挑選美食等），最後以 GUI 視窗化呈現，提升互動性。  

# 功能與操作  
* GUI 視窗化：  
  利用 Python 內建模組 Tkinter 製作。  
  <p align="center">
    <img width="800" src="https://github.com/KHchen183/MediaRepository/blob/main/CuisinePicking/Whole%20Win.png">
  </p>

* 口袋名單資料庫：  
  程式本身以 Excel 作為資料庫存取所有店家資訊，可於視窗中編輯、新增或移除，也可至後台 Excel 檔案進行資料處裡。

  <img width="480" src="https://github.com/KHchen183/MediaRepository/blob/main/CuisinePicking/Edit%20and%20Delete.gif">
  <img width="480" src="https://github.com/KHchen183/MediaRepository/blob/main/CuisinePicking/Add.gif">

* 網路搜尋美食資訊：  
  利用網路爬蟲抓取美食網站—[愛食記](https://ifoodie.tw/)的美食資訊，且可以將喜愛的店家資訊儲存至口袋名單。  
  1.搜尋美食資訊
  <p align="left">
    <img width="800" src="https://github.com/KHchen183/MediaRepository/blob/main/CuisinePicking/Search.gif">
  </p>  
  2.加入至清單中
  <p align="left">
    <img width="800" src="https://github.com/KHchen183/MediaRepository/blob/main/CuisinePicking/Add%20to%20database.gif">
  </p>
  
* 隨機挑選美食：  
  建立篩條件（如：種類、價位、縣市地區等），縮小挑選範圍，達到符合實際情況的可行性。  

# 技巧想法
* 多執行續：
  Tkinter 的視窗無法同時多功處理，在爬取網頁資料時，視窗無法進行其他操作，開一條執行續提供爬蟲搜尋資料。  
* 多核心：  
  爬蟲多筆店家資訊網頁，多核心縮短取得資料時間。  
* 視窗動態滾動區域(與靜態差異):  
