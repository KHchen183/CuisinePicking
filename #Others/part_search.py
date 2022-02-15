from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk    #藉助PIL模組來載入jpg、png圖片
from io import BytesIO            #將檔案暫存在記憶體中
import requests as req, bs4
import queue as qu
import threading as thd
import multiprocessing as mp
import time

#字樣類別與工具函式
class Rent():
  headers = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
  srch_opt1 = {"bg":"#C48888", "fg":"black", "font":("微軟正黑體", 12, "bold")}                                    #標籤：(分類、縣市、地區、排序)
  srch_opt2 = {"font":("微軟正黑體", 11)}                                                                          #選單、輸入：(分類、縣市、地區、排序)
  srch_opt3 = {"fg":"#BB5E00", "font":("微軟正黑體", 12, "bold")}                                                  #按鈕：(搜尋)
  srch_opt4 = {"fg":"#CE0000", "font":("微軟正黑體", 9, "bold")}                                                   #按鈕：(全部新增)
  srch_opt5 = {"bg":"#C48888", "activebackground":"#C48888", "fg":"#3C3C3C", "font":("微軟正黑體", 10, "bold")}    #按鈕：(上頁、下頁)
  srch_opt6 = {"bg":"#C48888", "fg":"#FCFCFC", "font":("Jokerman",14,"underline","bold")}                         #當前頁數
  srch_opt7 = {"bg":"#C48888", "fg":"#3C3C3C", "font":("微軟正黑體",11,"bold")}                                    #標籤：(價位)
  srch_opt8 = {"font":("微軟正黑體",9)}                                                                            #選單：(價位)
  srch_info1 = {"anchor":"e", "fg":"black", "font":("微軟正黑體", 15, "bold")}    
  srch_info2 = {"fg":"black", "font":("微軟正黑體", 15, "bold")}                  #店家名稱字樣
  srch_info3 = {"fg":"black", "font":("微軟正黑體", 11, "bold")}
  srch_info4 = {"fg":"black", "font":("微軟正黑體", 11)}

#多核心爬蟲實體物件
class Multicore_crwal():
  def __init__(self):
    self.nothing = None                 #待處理(這邊多餘的)
  def work(self, src, q):
    cpus = mp.cpu_count()               #當前設備的核心數
    # if cpus >= 4:
    #   cpus = 4
    pool = mp.Pool(processes = cpus)    #限制核心數
    multi_res = pool.map(self.job, src)
    pool.close()
    pool.join()
    q.put(multi_res)

  def job(self, urlsublist):
    #暫存圖片
    response = req.get(urlsublist[0], headers = Rent.headers)
    try:
      img_file = Image.open(BytesIO(response.content))
    except:
      img_file = Image.open("Image\\Waiting.jpg")
    img_file = img_file.resize((125, 105), Image.ANTIALIAS)
    print("img get!")
    #電話
    detail_response = req.get(urlsublist[1]).text                   
    detail_data = bs4.BeautifulSoup(detail_response, "html.parser").find("div", class_ = "main-content")
    try:                                                                  
      phone = detail_data.find("div", class_ = "phone-wrapper").find("span", class_ = "detail").a.getText()
      if phone[:2] != "09":
        phone = phone[:2]+"-"+phone[2:]
    except:
      phone = "尚無資訊"
    print("phone get!")
    return phone, img_file

#搜尋器實體物件
class app_search():
  def __init__(self, master):
    #一些重要資料的屬性
    self.win_search = master
    self.img_waiting = ImageTk.PhotoImage(Image.open("Image\\Waiting.png").resize((70, 70), Image.ANTIALIAS))      #預設圖片(Waiting)
    self.img_frame = ImageTk.PhotoImage(Image.open("Image\\Frame.png").resize((155, 130), Image.ANTIALIAS))        #預設圖片(Frame)
    self.img_heart = ImageTk.PhotoImage(Image.open("Image\\Heart.png").resize((25, 25), Image.ANTIALIAS))          #預設圖片(Heart)
    # self.img_crab = ImageTk.PhotoImage(Image.open("Image\\Crab.png").resize((25, 25), Image.ANTIALIAS))            #預設圖片(Crab)
    self.select_type = ["早餐","午餐","早午餐","下午茶","晚餐","宵夜","甜點","咖啡","燒烤","火鍋","小吃","酒吧","居酒屋","餐酒館",
                        "日本料理","義式料理","中式料理","韓式料理","泰式料理","美式料理","港式料理","約會餐廳","吃到飽","合菜",
                        "牛肉麵","牛排","拉麵","咖哩","素食","寵物友善","景觀餐廳","親子餐廳"]
    self.select_area = ["基隆市","台北市","新北市","桃園市","新竹市","新竹縣","苗栗縣","台中市","彰化縣","南投縣",
                        "雲林縣","嘉義市","嘉義縣","台南市","高雄市","屏東縣","台東縣","花蓮縣","宜蘭縣","澎湖縣"]
    self.select_sort = ["評價","人氣","最新"]
    self.price_level = ["不選擇","$150以下","$150~600","$600~1200","$1200以上"]
    self.lt_color = ["#D9B3B3", "#EBD6D6"]    #背景顏色切換
    self.frm_fd = {}                          #商店資訊的框架
    self.food_data = {}                       #商店的詳細資訊
    self.detail_data = []                     #商店的詳細頁面網址
    self.var_phone = {}                       #連結電話標籤的變數
    self.lb_img = {}                          #圖片的標籤(預設轉抓取呼叫用)
    self.btn_adds = {}                        #新增功能按鈕
    self.img_crawl = {}                       #存放抓取圖片檔案
    self.currentURL = ""                      #首頁網址
    self.prevURL = ""                         #上一頁網址
    self.nextURL = ""                         #下一頁網址
    
    #視窗頂部的操作框架(frm_opera)
    self.frm_opera = Frame(self.win_search, width = 560, height = 120, bg = "#C48888", borderwidth = 3, relief = "ridge")
    self.frm_opera.pack(side = "top", fill = "both")
    self.btn_search = Button(self.frm_opera, text = "搜尋",    **Rent.srch_opt3, command = self.first_search, borderwidth = 3, relief = "ridge")
    self.btn_search.place(anchor = "w", x = 500, y = 35, height = 35, width = 45)
    self.btn_add_all = Button(self.frm_opera, text = "全部\n新增", **Rent.srch_opt4, state = "disable", borderwidth = 3, relief = "ridge")
    self.btn_add_all.config(command = lambda input = self.food_data: self.add_to_database(input))
    self.btn_add_all.place(anchor = "w", x = 10, y = 85, height = 40, width = 40)
    self.btn_prevpage = Button(self.frm_opera, text = "上頁",    **Rent.srch_opt5, state = "disable", command = self.prev_crawl, relief = "flat")
    self.btn_prevpage.place(anchor = "w", x = 430, y = 85, height = 25, width = 35)
    self.btn_nextpage = Button(self.frm_opera, text = "下頁",    **Rent.srch_opt5, state = "disable", command = self.next_crawl, relief = "flat")
    self.btn_nextpage.place(anchor = "w", x = 505, y = 85, height = 25, width = 35)
    Label(self.frm_opera,  text = "分類:",   **Rent.srch_opt1).place(anchor = "w", x = 5, y = 35)
    Label(self.frm_opera,  text = "縣市:",   **Rent.srch_opt1).place(anchor = "w", x = 145, y = 35)
    Label(self.frm_opera,  text = "地區:",   **Rent.srch_opt1).place(anchor = "w", x = 270, y = 35)
    Label(self.frm_opera,  text = "排序:",   **Rent.srch_opt1).place(anchor = "w", x = 380, y = 35)
    Label(self.frm_opera,  text = "價位:",   **Rent.srch_opt7).place(anchor = "w", x = 60, y = 85)
    self.var_pagetxt = StringVar()
    self.var_pagetxt.set("♨")
    Label(self.frm_opera,  textvariable = self.var_pagetxt, **Rent.srch_opt6).place(anchor = "center", x = 485, y = 83)
    
    self.var_Typetxt = StringVar()
    self.cbb_Type = ttk.Combobox(self.frm_opera, **Rent.srch_opt2, textvariable = self.var_Typetxt, values = self.select_type, state = "normal")
    self.cbb_Type.place(anchor = "w", x = 50, y = 35, height = 25, width = 90)
    self.cbb_Type.current()

    self.var_Areatxt = StringVar()
    self.cbb_Area = ttk.Combobox(self.frm_opera, **Rent.srch_opt2, textvariable = self.var_Areatxt, values = self.select_area, state = "normal")
    self.cbb_Area.place(anchor = "w", x = 190, y = 35, height = 25, width = 75)
    self.cbb_Area.current()

    self.ety_SubArea = Entry(self.frm_opera, **Rent.srch_opt2, borderwidth = 1, relief = "sunken", state = "normal")
    self.ety_SubArea.place(anchor = "w", x = 315, y = 35, height = 23, width = 60)

    self.var_Sorttxt = StringVar()
    self.cbb_Sort = ttk.Combobox(self.frm_opera, **Rent.srch_opt2, textvariable = self.var_Sorttxt, values = self.select_sort, state = "normal")
    self.cbb_Sort.place(anchor = "w", x = 425, y = 35, height = 25, width = 60)
    self.cbb_Sort.current(0)

    self.var_Pricetxt = StringVar()
    self.cbb_Price = ttk.Combobox(self.frm_opera, **Rent.srch_opt8, textvariable = self.var_Pricetxt, values = self.price_level, state = "readonly")
    self.cbb_Price.place(anchor = "w", x = 105, y = 85, height = 20, width = 90)
    self.cbb_Price.current(0)

    self.progbar = ttk.Progressbar(self.frm_opera, orient = "horizontal", mode = "indeterminate", length = 210)
    self.progbar.place(anchor = "w", x = 210, y = 85)
    Button(self.frm_opera, text = "test", **Rent.srch_opt5 , command = self.test).place(anchor = "w", x = 150, y = 60)
    
    #建立搜尋資訊的框架(frm_foodinfo)
    self.frm_foodinfo = Frame(self.win_search, borderwidth = 3, relief = "ridge")
    self.frm_foodinfo.pack(side = "bottom", fill = "both", expand = 1)
    self.canv_main = Canvas(self.frm_foodinfo, bg = "#E1C4C4")                              #建立搜尋資訊的畫布(Canv_foodinfo)
    self.Y_Scrollbar = Scrollbar(self.frm_foodinfo)                                         #建立一個滾動條(在主視窗上)
    self.canv_main.config(yscrollcommand = self.Y_Scrollbar.set, highlightthickness = 0)    #配置畫布和滾動條
    self.Y_Scrollbar.config(orient = "vertical", width = 14, command = self.canv_main.yview)
    self.Y_Scrollbar.pack(fill = "y" ,side = "right", expand = False)
    self.canv_main.pack(fill = "both", expand = True)
    self.frm_assist = Frame(self.canv_main)                                                 #建立輔助框架(新增物件的區域)並配置在畫布上
    self.canv_main.create_window((0, 0), window = self.frm_assist, anchor = "nw")
    self.frm_assist.bind("<Enter>", self.bind_to_mousewheel)                                #設定框架內使用滾輪
    self.frm_assist.bind("<Leave>", self.unbind_to_mousewheel)                              #設定框架外解除滾輪                               

  def test(self):
    messagebox.askretrycancel(title = "連線異常!!!", message = "是否等待 3 秒後重新連線？", icon = "info")

  #首次搜尋
  def first_search(self):
    dict_sort = {"評價":"rating","人氣":"popular","最新":"recent"}
    dict_price = {"不選擇":"","$150以下":"priceLevel=1","$150~600":"priceLevel=2","$600~1200":"priceLevel=3","$1200以上":"priceLevel=4"}
    Area = "" if self.var_Areatxt.get() == "" else "/" + self.var_Areatxt.get()
    SubArea = "" if self.ety_SubArea.get() == "" else "/" + self.ety_SubArea.get()
    Fd_type = "" if self.var_Typetxt.get() == "" else "/" + self.var_Typetxt.get()
    Sort_by = "?sortby=" + dict_sort[self.var_Sorttxt.get()]
    Price_by = "" if dict_price[self.var_Pricetxt.get()] == "" else "&" + dict_price[self.var_Pricetxt.get()]
    self.currentURL = "https://ifoodie.tw/explore" + Area + SubArea +"/list" + Fd_type + Sort_by + Price_by
    self.multi_threads(self.currentURL)
    self.var_pagetxt.set(1)

  #上一頁
  def prev_crawl(self):
    self.multi_threads(self.prevURL)
    self.var_pagetxt.set(int(self.var_pagetxt.get()) - 1)

  #下一頁
  def next_crawl(self):
    self.multi_threads(self.nextURL)
    self.var_pagetxt.set(int(self.var_pagetxt.get()) + 1)

  #多執行緒搜尋
  def multi_threads(self, url):
    #進度條裝飾
    self.progbar.start(8)
    #先關閉按鈕四劍客(搜尋、新增、上頁、下頁)
    self.btn_add_all.config(state = "disable")
    self.btn_prevpage.config(state = "disable")
    self.btn_nextpage.config(state = "disable")
    self.btn_search.config(state = "disable")
    t_fisrt = thd.Thread(target = self.crawl_to_show, args = (url,))
    t_fisrt.start()

  #執行搜尋並顯示結果
  def crawl_to_show(self, url):
    #搜尋愛食記美食
    self.ifoodie_crawl(url)
    self.ifoodie_show()
    #進入多核心爬取電話和圖片
    try:
      q = qu.Queue()
      multicore = Multicore_crwal()
      multicore.work(self.detail_data, q)
      multicore_res = list(enumerate(q.get()))
      for item in multicore_res:
        self.food_data[item[0]]["phone"] = item[1][0]
        self.var_phone[item[0]].set(self.food_data[item[0]]["phone"])
        self.img_crawl[item[0]] = ImageTk.PhotoImage(item[1][1])
        self.lb_img[item[0]].config(bg = "#272727", image = self.img_crawl[item[0]])
        self.btn_adds[item[0]].config(state = "normal")
    except:
      Ans = messagebox.askretrycancel(title = "連線異常!!!", message = "是否等待 5 秒後重新連線？", icon = "info")
      if Ans == True:
        time.sleep(5)
        self.crawl_to_show(url)
      else:
        pass
    self.check_pageBTN()
    self.progbar.stop()

  #搜尋愛食記美食(爬蟲)
  def ifoodie_crawl(self, url):
    self.food_data.clear()      #清空暫存資料
    self.detail_data.clear()    #清空暫存資料
    count = 0                   #計數
    try:
      req_data = req.get(url, headers = Rent.headers).text
    except:
      time.sleep(5)
      self.ifoodie_crawl(url)
    entire_data = bs4.BeautifulSoup(req_data, "html.parser")
    items = entire_data.find_all("div", class_ = "restaurant-info")
    #上一頁
    try:
      self.prevURL = "https://ifoodie.tw" + entire_data.find("a", string="上一頁")["href"]      #上一頁網址
    except:
      self.prevURL = ""
    #下一頁
    try:
      self.nextURL = "https://ifoodie.tw" + entire_data.find("a", string="下一頁 ›")["href"]    #下一頁網址
    except:
      self.nextURL = ""
    #店家資訊
    for item in items:
      get_title = item.find("a", class_ = "title-text")                                                   
      #店家名稱
      title = get_title.getText()                                           
      #評價(問題:可能查無資料)
      try:                                                                  
        rank = item.find("div", class_ = "text").getText()     
      except:
        rank = "尚無資訊"
      #地址
      try:                                                                  
        address = item.find("div", class_ = "address-row").getText()               
      except:
        address = "尚無資訊"
      #營業時間
      try:                                                                  
        open_time = item.find("div", class_ = "info").getText().split()
        if open_time[0] ==  "尚無營業時間資訊" or open_time[0] == "今日休息":
          open_time = [open_time[0]]
        else:
          open_time = open_time[1:]
      except:
        open_time = "尚無資訊"
      #平均消費
      try:                                                                  
        avg_price = item.find("div", class_ = "avg-price").getText()[5:]    
      except:
        avg_price = "尚無資訊"
      #所有種類   
      categorybox = item.find("div", class_ = "category-row").find_all("a", class_ = "category")
      category = []
      for cate in categorybox:
        cate = cate.getText()
        if cate != "附近餐廳":
          category.append(cate)
      #取得該店家圖片的網址(待提供多核心搜尋)
      try:                                                                  
        img_url = item.a.img
        if img_url.has_attr("data-src"):
          img_url = img_url["data-src"]
        else:
          img_url = img_url["src"]   
      except:
        img_url = "Wrong"
      #取得該店家詳細資訊的網址(待提供多核心搜尋)
      detail_url = "https://ifoodie.tw" + get_title["href"]
      #暫存資訊
      self.food_data[count] = {"title":title,"rank":rank,"avg_price":avg_price,"open_time":open_time,"address":address,"category":category}
      self.detail_data.append([img_url, detail_url])
      count+=1
  
  #初步顯示並製作店家資訊框架
  def ifoodie_show(self): 
    self.clear_frm_assist()
    for num in self.food_data:
      #顯示框架
      color = self.lt_color[num % 2]
      self.frm_fd[num] = Frame(self.frm_assist, width = 540, height = 180, bg = color)
      self.frm_fd[num].grid(row = num, column = 0)
      Frame(self.frm_fd[num], width = 40,  height = 180, bg = color, borderwidth = 2, relief = "ridge").pack(side = "left",  fill = "both", expand = 1)    #裝飾用框架
      Frame(self.frm_fd[num], width = 500, height = 180, bg = color, borderwidth = 2, relief = "ridge").pack(side = "right", fill = "both", expand = 1)    #裝飾用框架
      #顯示標籤
      Label(self.frm_fd[num], text = f"{num+1}.", **Rent.srch_info1, width = 2 ,bg = color).place(x = 50, y = 8)
      Label(self.frm_fd[num], text = "評價:",     **Rent.srch_info3, width = 4 ,bg = color).place(x = 205, y = 45)
      Label(self.frm_fd[num], text = "均消:",     **Rent.srch_info3, width = 4 ,bg = color).place(x = 205, y = 70)
      Label(self.frm_fd[num], text = "電話:",     **Rent.srch_info3, width = 4 ,bg = color).place(x = 205, y = 95)
      Label(self.frm_fd[num], text = "時間:",     **Rent.srch_info3, width = 4 ,bg = color).place(x = 205, y = 120)
      Label(self.frm_fd[num], text = "地址:",     **Rent.srch_info3, width = 4 ,bg = color).place(x = 205, y = 145)
      #顯示資訊
      Label(self.frm_fd[num], text = self.food_data[num]["title"],     **Rent.srch_info2, bg = color).place(x = 82, y = 8)
      Label(self.frm_fd[num], text = self.food_data[num]["rank"] + " ★",      **Rent.srch_info4, bg = color).place(x = 250, y = 45)
      Label(self.frm_fd[num], text = self.food_data[num]["avg_price"], **Rent.srch_info4, bg = color).place(x = 250, y = 70)
      Label(self.frm_fd[num], text = self.food_data[num]["open_time"][:3], **Rent.srch_info4, bg = color).place(x = 250, y = 120)
      Label(self.frm_fd[num], text = self.food_data[num]["address"],   **Rent.srch_info4, bg = color).place(x = 250, y = 145)
      self.var_phone[num] = StringVar()
      self.var_phone[num].set("請稍後...")
      Label(self.frm_fd[num], textvariable = self.var_phone[num], **Rent.srch_info4, bg = color).place(x = 250, y = 95)
      Label(self.frm_fd[num], bg = color, image = self.img_frame).place(anchor = "center", x = 123, y = 109)
      self.lb_img[num] = Label(self.frm_fd[num], bg = color, image = self.img_waiting)
      self.lb_img[num].place(anchor = "center", x = 125, y = 108)
      #顯示新增按鈕
      self.btn_adds[num] = Button(self.frm_fd[num], activebackground = color, image = self.img_heart, relief = "flat", state = "disable", bg = color)
      self.btn_adds[num].config(command = lambda input = self.food_data[num]: self.add_to_database(input))
      self.btn_adds[num].place(anchor = "center", x = 20, y = 90)
    self.update_Scrollregion()

  #新增功能按鈕
  def add_to_database(self, data):
    print(data)

  #重置商店資訊的框架
  def clear_frm_assist(self):
    for widget in self.frm_assist.winfo_children():
      widget.destroy()          #永久移除
      # widget.grid_forget()    #暫時隱藏(多次搜尋會造成視窗移動延遲)
    self.frm_fd.clear()

  #更新滾動區域
  def update_Scrollregion(self):
    self.canv_main.update_idletasks()
    self.canv_main.config(scrollregion = self.frm_assist.bbox())
  
  #檢查上下頁按鈕
  def check_pageBTN(self):
    if self.prevURL == "":
      self.btn_prevpage["state"] = "disable"
    else:
      self.btn_prevpage["state"] = "normal"

    if self.nextURL == "":
      self.btn_nextpage["state"] = "disable"
    else:
      self.btn_nextpage["state"] = "normal"

    if self.food_data == {}:
      self.btn_add_all.config(state = "disable")
    else:
      self.btn_add_all.config(state = "normal")
    #搜尋按鈕直接打開
    self.btn_search.config(state = "normal")
  
  #滾輪在框架區域中
  def bind_to_mousewheel(self, event):
    self.canv_main.bind_all("<MouseWheel>", self.on_mousewheel)
  #滾輪不在框架區域中
  def unbind_to_mousewheel(self, event):
    self.canv_main.unbind_all("<MouseWheel>")  
  #在畫布上使用滾輪
  def on_mousewheel(self, event):
    self.canv_main.yview_scroll(int(-1*(event.delta//120)), "units")

if __name__ == "__main__":
  #建立主視窗
  win_search = Tk()
  win_search.title("Searching Top Food")
  win_search.geometry("560x960+960+30")
  win_search.resizable(0, 0)
  window_search = app_search(win_search)
  win_search.mainloop()