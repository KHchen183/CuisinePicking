#For Python 3.9.7
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk    #藉助 PIL 模組來載入 jpg、png 圖片
from io import BytesIO            #將檔案暫存在記憶體中
import time
import pandas as pd
import random
import requests as req, bs4
import queue as qu
import threading as thd
import multiprocessing as mp

#字樣類別與工具函式
class Rent():
  #隨機選擇主視窗
  root_info1 = {"bg":"#ADD8E6","fg":"black","font":("微軟正黑體",12,"bold")}                #隨機框架標籤
  root_info2 = {"bg":"#D1E9E9","fg":"#9F5000","font":("微軟正黑體",12,"bold"),              #隨機框架文字框
                "bd":"0","padx":"5","height":1,"width":28}
  root_info3 = {"font":("微軟正黑體",9),"state":"readonly"}                                 #篩選：(種類、均消、縣市)
  root_info4 = {"fg":"black","font":("微軟正黑體",11)}                                      #篩選：(地區)
  root_info5 = {"bg":"#E0E0E0","fg":"#BB3D00","font":("微軟正黑體",14,"bold")}              #按鈕：(執行、搜尋)
  root_info6 = {"fg":"#272727","bd":2,"relief":"groove","font":("微軟正黑體",10,"bold")}    #按鈕：(新增、編輯、刪除)
  root_info7 = {"fg":"#616130","font":("微軟正黑體",11,"bold")}                             #新增/編輯視窗文字
  root_info7_1 = {"fg":"#FF2D2D","font":("微軟正黑體",11,"bold")}                           #新增/編輯視窗文字特別標記
  root_info7_2 = {"fg":"#CE0000","font":("微軟正黑體",11,"bold")}                           #視窗文字內按鈕：(新增、修改)
  root_info8 = {"fg":"#4F4F4F","font":("微軟正黑體",8)}                                     #提示標語
  #愛食記搜尋器
  headers = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
  srch_opt1 = {"bg":"#C48888","fg":"black", "font":("微軟正黑體",12,"bold")}                                    #標籤：(分類、縣市、地區、排序)
  srch_opt2 = {"font":("微軟正黑體",11)}                                                                        #選單、輸入：(分類、縣市、地區、排序)
  srch_opt3 = {"fg":"#BB5E00","font":("微軟正黑體",12,"bold")}                                                  #按鈕：(搜尋)
  srch_opt4 = {"fg":"#CE0000","font":("微軟正黑體",9,"bold")}                                                   #按鈕：(全部新增)
  srch_opt5 = {"bg":"#C48888","activebackground":"#C48888", "fg":"#3C3C3C", "font":("微軟正黑體",10,"bold")}    #按鈕：(上頁、下頁)
  srch_opt6 = {"bg":"#C48888","fg":"#FCFCFC","font":("Jokerman",14,"underline","bold")}                        #當前頁數
  srch_opt7 = {"bg":"#C48888","fg":"#3C3C3C","font":("微軟正黑體",11,"bold")}                                   #標籤：(均消)
  srch_opt8 = {"font":("微軟正黑體",9)}                                                                         #選單：(均消)
  srch_info1 = {"anchor":"e","fg":"black","font":("微軟正黑體",15,"bold")}                                      #店家編號
  srch_info2 = {"fg":"black","font":("微軟正黑體",15,"bold")}                                                   #標籤：(店家名稱)
  srch_info3 = {"fg":"black","font":("微軟正黑體",11,"bold")}                                                   #標籤：(評價、均消、電話、時間、地址)
  srch_info4 = {"fg":"black","font":("微軟正黑體",11)}                                                          #標籤：(評價、均消、電話、時間、地址)資訊

  #食物資訊微處理
  def fd_refresh(Is_reset):
    global EX_database, all_Category
    #均消轉 int 型態
    for num in range(EX_database.shape[0]):
      temp = EX_database.loc[num]["AvgPrice"]
      if temp != "尚無資訊":
        EX_database.loc[num,"AvgPrice"] = int(temp)

    #新增、移除
    if Is_reset:
      all_Category = []
    for num in range(EX_database.shape[0]):
      if pd.isna(EX_database.loc[num]["Category"]):
        EX_database.loc[num,"Category"] = ""
      else:
        temp_category = EX_database.loc[num]["Category"].split()
        for element in temp_category:
          if element not in all_Category:
            all_Category.append(element)
  
  def save_database():
    global EX_database
    save_EX_data = EX_database.set_index("Name")
    save_EX_data.to_excel("Database//Cuisine_data.xlsx")

#主介面實體物件
class app_main():
  def __init__(self, master):
    #一些重要資料的屬性
    self.win_root = master
    style = ttk.Style()                                              #加入樣式
    style.theme_use("vista")
    style.configure("Treeview",                                      #資訊欄配置
                    font = ("微軟正黑體", 11, "bold"),
                    foreground = "black",
                    rowheight = 35)
                    # background = "#F3F3FA"
                    # fieldbackground = "red"
    style.configure("Treeview.Heading",                              #標題欄配置
                    font = ("微軟正黑體", 12, "bold"),
                    foreground = "#3D7878")
                    # background = "#8F4586"   
    style.map("Treeview", background = [("selected", "#A5A552")])    #選取顏色
    #DataBase
    global EX_database, all_Category
    self.first_database = EX_database
    self.root_slcpriceLV= ["不選擇","$150以下","$150~600","$600~1200","$1200以上"]
    self.root_slcarea = ["不選擇","基隆市","台北市","新北市","桃園市","新竹市","新竹縣","苗栗縣","台中市","彰化縣","南投縣",
                         "雲林縣","嘉義市","嘉義縣","台南市","高雄市","屏東縣","台東縣","花蓮縣","宜蘭縣","澎湖縣"]
    #建立菜單
    self.menu_root = Menu(self.win_root)
    self.win_root.config(menu = self.menu_root)
    self.menu_file = Menu(self.menu_root, tearoff = False)
    self.menu_root.add_cascade(label = "檔案", menu = self.menu_file)
    self.menu_file.add_cascade(label = "儲存", command = lambda input = False:self.save_msg(input))
    self.menu_file.add_cascade(label = "作者", command = self.show_author)
    self.menu_file.add_separator()
    self.menu_file.add_cascade(label = "離開", command = win_root.quit)

    #建立主框架
    self.frm_main = Frame(self.win_root, bg = "#D9B3B3", borderwidth = 2, relief = "ridge")
    self.frm_main.pack(fill = "both", expand = True)
    
    #建立隨機顯示框架
    self.frm_showrand = LabelFrame(self.frm_main, text = " 讓命運安排吧 ")
    self.frm_showrand.config(bg = "#ADD8E6", fg = "#FF5151", bd = 3, relief = "ridge", font = ("微軟正黑體", 14, "bold"))
    self.frm_showrand.place(anchor = "nw", x = 15, y = 15, height = 285, width = 580)
    #建立標籤
    Label(self.frm_showrand, text = "名 稱:", **Rent.root_info1, width = 6).place(anchor = "w", x = 5, y = 25)
    Label(self.frm_showrand, text = "評 價:", **Rent.root_info1, width = 6).place(anchor = "w", x = 5, y = 65)
    Label(self.frm_showrand, text = "均 消:", **Rent.root_info1, width = 6).place(anchor = "w", x = 5, y = 105)
    Label(self.frm_showrand, text = "電 話:", **Rent.root_info1, width = 6).place(anchor = "w", x = 5, y = 145)
    Label(self.frm_showrand, text = "時 間:", **Rent.root_info1, width = 6).place(anchor = "w", x = 5, y = 185)
    Label(self.frm_showrand, text = "地 址:", **Rent.root_info1, width = 6).place(anchor = "w", x = 5, y = 225)
    Label(self.frm_showrand, text = "篩選種類:", **Rent.root_info1, width = 8).place(anchor = "w", x = 380, y = 50)
    Label(self.frm_showrand, text = "篩選均消:", **Rent.root_info1, width = 8).place(anchor = "w", x = 380, y = 100)
    Label(self.frm_showrand, text = "篩選縣市:", **Rent.root_info1, width = 8).place(anchor = "w", x = 380, y = 150)
    Label(self.frm_showrand, text = "鄉鎮市區:", **Rent.root_info1, width = 8).place(anchor = "w", x = 380, y = 200)
    #建立文字框
    self.txt_name = Text(self.frm_showrand, **Rent.root_info2)
    self.txt_name.place(anchor = "w", x = 70, y = 25)
    self.txt_rank = Text(self.frm_showrand, **Rent.root_info2)
    self.txt_rank.place(anchor = "w", x = 70, y = 65)
    self.txt_avgprice = Text(self.frm_showrand, **Rent.root_info2)
    self.txt_avgprice.place(anchor = "w", x = 70, y = 105)
    self.txt_phone = Text(self.frm_showrand, **Rent.root_info2)
    self.txt_phone.place(anchor = "w", x = 70, y = 145)
    self.txt_opentime = Text(self.frm_showrand, **Rent.root_info2)
    self.txt_opentime.place(anchor = "w", x = 70, y = 185)
    self.txt_address = Text(self.frm_showrand, **Rent.root_info2)
    self.txt_address.place(anchor = "w", x = 70, y = 225)
    #建立篩選的選單
    self.var_slcTypetxt = StringVar()
    self.cbb_slcType = ttk.Combobox(self.frm_showrand, textvariable = self.var_slcTypetxt, **Rent.root_info3, values = ["不選擇"] + all_Category)
    self.cbb_slcType.place(anchor = "w",x = 470, height = 25, y = 50, width = 90)
    self.cbb_slcType.current(0)

    self.var_slcPricetxt = StringVar()
    self.cbb_slcPrice = ttk.Combobox(self.frm_showrand, textvariable = self.var_slcPricetxt, **Rent.root_info3, values = self.root_slcpriceLV)
    self.cbb_slcPrice.place(anchor = "w",x = 470, height = 25, y = 100, width = 90)
    self.cbb_slcPrice.current(0)

    self.var_slcAreatxt = StringVar()
    self.cbb_slcArea = ttk.Combobox(self.frm_showrand, textvariable = self.var_slcAreatxt, **Rent.root_info3, values = self.root_slcarea)
    self.cbb_slcArea.place(anchor = "w",x = 470, y = 150, height = 25, width = 90)
    self.cbb_slcArea.current(0)

    self.ety_slcSubArea = Entry(self.frm_showrand, **Rent.root_info4, relief = "flat", state = "normal")
    self.ety_slcSubArea.place(anchor = "w", x = 470, y = 200, height = 23, width = 90)

    Label(self.frm_showrand, bg = "#ADD8E6", text = "注: \"臺\" → \"台\"", **Rent.root_info8).place(x = 470, y = 215, height = 15, width = 80)
    
    #建立"執行"的按鈕
    self.btn_randpick = Button(self.frm_main, text = "隨機\n挑選", **Rent.root_info5, bd = 3, relief = "ridge", command = self.pick_one)
    self.btn_randpick.place(anchor = "center", x = 675, y = 120, height = 100, width = 100)
    #建立"搜尋愛食記"的按鈕
    self.btn_ifoodie = Button(self.frm_main, text = "搜尋 ➜", **Rent.root_info5, bd = 3, relief = "ridge", command = self.srch_ifoodie)
    self.btn_ifoodie.place(anchor = "center", x = 675, y = 230, height = 50, width = 100)
  
    #建立資訊框架
    self.lbfrm_showdata = LabelFrame(self.frm_main, text = " 美食口袋名單 ")
    self.lbfrm_showdata.config(bg = "#ADD8E6", fg = "#FF5151", bd = 3, relief = "ridge", font = ("微軟正黑體", 14, "bold"))
    self.lbfrm_showdata.place(anchor = "nw", x = 15, y = 320, height = 600, width = 720)
    self.btn_add = Button(self.lbfrm_showdata, text = "新增", command = self.add_treevdata, **Rent.root_info6)
    self.btn_add.place(anchor = "center", x = 570, y = 10, height = 30, width = 38)
    self.btn_edit = Button(self.lbfrm_showdata, text = "編輯", command = self.edit_treevdata, **Rent.root_info6)
    self.btn_edit.place(anchor = "center", x = 620, y = 10, height = 30, width = 38)
    self.btn_delete = Button(self.lbfrm_showdata, text = "移除", command = self.clr_treevdata, **Rent.root_info6)
    self.btn_delete.place(anchor = "center", x = 670, y = 10, height = 30, width = 38)
    #建立樹狀列表
    self.treev_info = ttk.Treeview(self.lbfrm_showdata, selectmode = "extended")
    self.treev_info.place(x = 5, y = 30, height = 523, width = 692)
    self.tvY_Scroll = Scrollbar(self.lbfrm_showdata, orient = "vertical", width = 13, command = self.treev_info.yview)
    self.tvY_Scroll.place(x = 695, y = 30, height = 527)
    self.tvX_Scroll = Scrollbar(self.lbfrm_showdata, orient = "horizontal", width = 13, command = self.treev_info.xview)
    self.tvX_Scroll.place(x = 5, y = 544, width = 690)
    self.treev_info.config(yscrollcommand = self.tvY_Scroll.set, xscrollcommand = self.tvX_Scroll.set)
    #定義樹狀列表
    self.treev_define()    
    #打叉叉後執行
    win_root.protocol('WM_DELETE_WINDOW', lambda input = True:self.save_msg(input))    

  #定義樹狀列表
  def treev_define(self):
    # self.treev_info["show"] = "headings"
    self.treev_info["column"] = ["Name","Rank","AvgPrice","Phone","OpenTime",
                                 "Address","Category","Area","SubArea"]
    #格式化欄位
    self.treev_info.column("#0", width = 25, minwidth = 25, stretch = False)
    self.treev_info.column("Name", width = 225, minwidth = 225, stretch = False)
    self.treev_info.column("Rank", width = 50, minwidth = 50, stretch = False, anchor = "center")
    self.treev_info.column("AvgPrice", width = 70, minwidth = 70, stretch = False, anchor = "e")
    self.treev_info.column("Phone", width = 110, minwidth = 110, stretch = False, anchor = "w")
    self.treev_info.column("OpenTime", width = 200, minwidth = 200, stretch = False)
    self.treev_info.column("Address", width = 260, minwidth = 260, stretch = False)
    self.treev_info.column("Category", width = 260, minwidth = 260, stretch = False)
    self.treev_info.column("Area", width = 70, minwidth = 70, stretch = False)
    self.treev_info.column("SubArea", width = 70, minwidth = 70, stretch = False)
    self.treev_info.heading("Name", text = "店家名稱")
    self.treev_info.heading("Rank", text = "評價")
    self.treev_info.heading("AvgPrice", text = "均消")
    self.treev_info.heading("Phone", text = "電話")
    self.treev_info.heading("OpenTime", text = "營業時間")
    self.treev_info.heading("Address", text = "地址")
    self.treev_info.heading("Category", text = "種類")
    self.treev_info.heading("Area", text = "縣市")
    self.treev_info.heading("SubArea", text = "地區")
    self.data_to_treev()
  
  #樹狀列表更新全部資料
  def data_to_treev(self):
    global EX_database
    df = EX_database
    self.treev_info.tag_configure("evenrow", background = "#F3F3FA")
    self.treev_info.tag_configure("oddrow", background = "#F2E6E6")
    #先全部清除
    for item in self.treev_info.get_children():
      self.treev_info.delete(item)
    #再加入資料
    for i in df.index:    #.index = RangeIndex(start=0, stop=end, step=1)
      if i % 2 == 0:
        self.treev_info.insert("", "end", iid = i, values = list(df.iloc[i]), tags = "evenrow")
      else:
        self.treev_info.insert("", "end", iid = i, values = list(df.iloc[i]), tags = "oddrow")
    # self.treev_info.insert("0", "end", values = ("","","","","test open time"))    #附屬資料(未來可新增)
  
  #新增樹狀列表資料
  def add_treevdata(self):
    #關閉"新增"視窗
    def win_destroy():    
      self.btn_add.config(state = "normal")
      self.btn_edit.config(state = "normal")
      self.btn_delete.config(state = "normal")
      win_add.destroy() 
    #新增按鈕(儲存後離開)
    def add_info():
      global EX_database
      temp_name = txt_na.get("1.0","end-1c")
      temp_address = txt_add.get("1.0","end-1c")
      if txt_avg.get("1.0","end-1c") == "":
        temp_avgprice = "尚無資訊"
      else:
        temp_avgprice = txt_avg.get("1.0","end-1c")

      if temp_name.replace(" ","") == "" or temp_address.replace(" ","") == "":    #至少輸入名稱和地址
        messagebox.showinfo(title = "提示", message = "請至少輸入店家名稱與地址的資訊!!", parent = win_add)
      else:
        duplication = False    #資料是否重複
        for item in EX_database["Address"]:
          if item == temp_address:
            duplication = True
            messagebox.showinfo(title = "重複的店家資訊", message = "具有相同地址的店家資訊，請檢查資料是否重複!!", parent = win_add)
            break
        if duplication == False:
          Ans = messagebox.askyesno(title = "新增店家資訊", message = "確定新增店家資訊？", parent = win_add)
          if Ans:
            #篩選出縣市、地區的資料
            temp_address = temp_address.replace("臺","台")
            c1 = 0
            for s1 in temp_address:
              c1 += 1
              if s1 == "市":
                temp = temp_address[c1:]
                c2 = 0
                for s2 in temp:
                  c2 += 1
                  if s2 == "區":
                    break
                break
              if s1 == "縣":
                temp = temp_address[c1:]
                c2 = 0
                for s2 in temp:
                  c2 += 1
                  if s2 == "鄉" or s2 == "鎮" or s2 == "市":
                    break
                break
            #建立 new DataFrame
            new_data = pd.DataFrame({"Name":[temp_name],
                                    "Rank":[txt_ra.get("1.0","end-1c")],
                                    "AvgPrice":temp_avgprice,
                                    "Phone":[txt_ph.get("1.0","end-1c")],
                                    "OpenTime":[txt_op.get("1.0","end-1c")],
                                    "Address":[temp_address],
                                    "Category":[txt_cate.get("1.0","end-1c")],
                                    "Area":[temp_address[c1-3:c1]],
                                    "SubArea":[temp[:c2]]})
            EX_database = EX_database.append(new_data, ignore_index = True)    #新增到 DataBase 中
            self.data_to_treev()
            win_destroy()
            #更新篩選條件的資料
            Rent.fd_refresh(Is_reset = False)
            self.cbb_slcType.config(values = ["不選擇"] + all_Category)

    #建立"新增"的視窗
    self.btn_add.config(state = "disable")
    self.btn_edit.config(state = "disable")
    self.btn_delete.config(state = "disable")
    win_add = Toplevel(self.win_root)
    win_add.title("新增店家的詳細資訊")
    win_add.geometry("340x260+600+120")
    win_add.attributes("-topmost", True)#置頂
    win_add.resizable(0, 0)
    Label(win_add, text = "名 稱:", **Rent.root_info7_1).grid(row = 0, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "地 址:", **Rent.root_info7_1).grid(row = 1, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "評 價:", **Rent.root_info7).grid(row = 2, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "均 消:", **Rent.root_info7).grid(row = 3, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "電 話:", **Rent.root_info7).grid(row = 4, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "時 間:", **Rent.root_info7).grid(row = 5, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "種 類:", **Rent.root_info7).grid(row = 6, column = 0, padx = 5, pady = 3)
    Label(win_add, text = "注: 請至少輸入\n\"名稱\"與\"地址\"", **Rent.root_info8).place(x = 10, y = 220, height = 30, width = 80)
    txt_na = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_na.grid(row = 0, column = 1, padx = 5, pady = 3)
    txt_add = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_add.grid(row = 1, column = 1, padx = 5, pady = 3)
    txt_ra = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_ra.grid(row = 2, column = 1, padx = 5, pady = 3)
    txt_avg = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_avg.grid(row = 3, column = 1, padx = 5, pady = 3)
    txt_ph = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_ph.grid(row = 4, column = 1, padx = 5, pady = 3)
    txt_op = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_op.grid(row = 5, column = 1, padx = 5, pady = 3)
    txt_cate = Text(win_add, **Rent.root_info7 ,height = 1, width = 30)
    txt_cate.grid(row = 6, column = 1, padx = 5, pady = 3)
    Button(win_add, text = "新增", command = add_info, **Rent.root_info7_2).place(anchor = "center", x = 170, y = 235, height = 30)
    win_add.protocol('WM_DELETE_WINDOW', win_destroy)    #打叉叉後執行

  #編輯樹狀列表資料
  def edit_treevdata(self):
    global EX_database, all_Category
    #關閉"編輯"視窗
    def win_destroy():    
      self.btn_add.config(state = "normal")
      self.btn_edit.config(state = "normal")
      self.btn_delete.config(state = "normal")
      win_edit.destroy() 
    #修改按鈕(儲存後離開)
    def modify():
      Ans = messagebox.askyesno(title = "修改店家資訊", message = "確定修改店家資訊？", parent = win_edit)
      if Ans:
        if txt_avg.get("1.0","end-1c") == "":
          temp_avgprice = "尚無資訊"
        else:
          temp_avgprice = txt_avg.get("1.0","end-1c")
        EX_database.loc[temp_index,"Name"] = txt_na.get("1.0","end-1c")    #文字框最後一個字元是"\n"，所以要減去一個字元
        EX_database.loc[temp_index,"Rank"] = txt_ra.get("1.0","end-1c")
        EX_database.loc[temp_index,"AvgPrice"] = temp_avgprice
        EX_database.loc[temp_index,"Phone"] = txt_ph.get("1.0","end-1c")
        EX_database.loc[temp_index,"OpenTime"] = txt_op.get("1.0","end-1c")
        EX_database.loc[temp_index,"Address"] = txt_add.get("1.0","end-1c")
        EX_database.loc[temp_index,"Category"] = txt_cate.get("1.0","end-1c")
        EX_database.loc[temp_index,"Area"] = txt_ar.get("1.0","end-1c")
        EX_database.loc[temp_index,"SubArea"] = txt_sbar.get("1.0","end-1c")
        self.data_to_treev()
        win_destroy()
        #更新篩選條件的資料
        Rent.fd_refresh(Is_reset = True)
        self.cbb_slcType.config(values = ["不選擇"] + all_Category)

    selected_index = self.treev_info.selection()
    if len(selected_index) == 1:
      temp_index = int(selected_index[0])
      #建立"編輯"的視窗
      self.btn_add.config(state = "disable")
      self.btn_edit.config(state = "disable")
      self.btn_delete.config(state = "disable")
      win_edit = Toplevel(self.win_root)
      temp_title = EX_database.loc[temp_index]["Name"]
      win_edit.title(f"{temp_title}的詳細資訊")
      win_edit.geometry("340x315+600+100")
      win_edit.attributes("-topmost", True)#置頂
      win_edit.resizable(0, 0)
      Label(win_edit, text = "名 稱:", **Rent.root_info7).grid(row = 0, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "評 價:", **Rent.root_info7).grid(row = 1, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "均 消:", **Rent.root_info7).grid(row = 2, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "電 話:", **Rent.root_info7).grid(row = 3, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "時 間:", **Rent.root_info7).grid(row = 4, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "地 址:", **Rent.root_info7).grid(row = 5, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "種 類:", **Rent.root_info7).grid(row = 6, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "縣 市:", **Rent.root_info7).grid(row = 7, column = 0, padx = 5, pady = 3)
      Label(win_edit, text = "地 區:", **Rent.root_info7).grid(row = 8, column = 0, padx = 5, pady = 3)
      txt_na = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_na.grid(row = 0, column = 1, padx = 5, pady = 3)
      txt_ra = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_ra.grid(row = 1, column = 1, padx = 5, pady = 3)
      txt_avg = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_avg.grid(row = 2, column = 1, padx = 5, pady = 3)
      txt_ph = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_ph.grid(row = 3, column = 1, padx = 5, pady = 3)
      txt_op = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_op.grid(row = 4, column = 1, padx = 5, pady = 3)
      txt_add = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_add.grid(row = 5, column = 1, padx = 5, pady = 3)
      txt_cate = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_cate.grid(row = 6, column = 1, padx = 5, pady = 3)
      txt_ar = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_ar.grid(row = 7, column = 1, padx = 5, pady = 3)
      txt_sbar = Text(win_edit, **Rent.root_info7 ,height = 1, width = 30)
      txt_sbar.grid(row = 8, column = 1, padx = 5, pady = 3)
      txt_na.insert("insert", EX_database.loc[temp_index]["Name"])
      txt_ra.insert("insert", EX_database.loc[temp_index]["Rank"])
      txt_avg.insert("insert", EX_database.loc[temp_index]["AvgPrice"])
      txt_ph.insert("insert", EX_database.loc[temp_index]["Phone"])
      txt_op.insert("insert", EX_database.loc[temp_index]["OpenTime"])
      txt_add.insert("insert", EX_database.loc[temp_index]["Address"])
      txt_cate.insert("insert", EX_database.loc[temp_index]["Category"])
      txt_ar.insert("insert", EX_database.loc[temp_index]["Area"])
      txt_sbar.insert("insert", EX_database.loc[temp_index]["SubArea"])
      Button(win_edit, text = "修改", command = modify, **Rent.root_info7_2).place(anchor = "center", x = 170, y = 295, height = 30)
      win_edit.protocol('WM_DELETE_WINDOW', win_destroy)    #打叉叉後執行
    elif len(selected_index) == 0:
      pass
    else:
      messagebox.showinfo(title = "提示", message = "一次僅可選擇一筆資料進行編輯!!", parent = self.win_root)

  #刪除樹狀列表資料
  def clr_treevdata(self):
    global EX_database, all_Category
    selected_index = list(map(int, self.treev_info.selection()))
    if selected_index == []:
      pass
    else:
      EX_database.drop(selected_index, axis = 0, inplace = True)
      EX_database.reset_index(inplace = True, drop = True)
      self.data_to_treev()
      #更新篩選條件的資料
      Rent.fd_refresh(Is_reset = True)
      self.cbb_slcType.config(values = ["不選擇"] + all_Category)

  #執行隨機美食
  def pick_one(self):
    global EX_database
    filted_data = EX_database
    get_slcType = self.var_slcTypetxt.get()
    get_slcPrice = self.var_slcPricetxt.get()
    get_slcArea = self.var_slcAreatxt.get()
    get_slcSubArea = self.ety_slcSubArea.get()
    if get_slcType != "不選擇":
      filted_data = filted_data.loc[filted_data["Category"].str.split().apply(lambda f: get_slcType in f)]               #篩選"Type"
    if get_slcPrice != "不選擇":
      if get_slcPrice == "$150以下":
        filted_data = filted_data.loc[filted_data["AvgPrice"].apply(lambda f: f <= 150 if f != "尚無資訊" else False)]    #篩選"AvgPrice"
      elif get_slcPrice == "$150~600":
        filted_data = filted_data.loc[filted_data["AvgPrice"].apply(lambda f: 150 < f <= 600 if f != "尚無資訊" else False)]
      elif get_slcPrice == "$600~1200":
        filted_data = filted_data.loc[filted_data["AvgPrice"].apply(lambda f: 600 < f <= 1200 if f != "尚無資訊" else False)]
      else:
        filted_data = filted_data.loc[filted_data["AvgPrice"].apply(lambda f: 1200 < f if f != "尚無資訊" else False)]
    if get_slcArea != "不選擇":
      filted_data = filted_data.loc[filted_data["Area"].apply(lambda f: f == get_slcArea)]                               #篩選"Area"
    if get_slcSubArea != "":
      filted_data = filted_data.loc[filted_data["SubArea"].apply(lambda f: f == get_slcSubArea)]                         #篩選"SubArea"
    if filted_data.shape[0] == 0:
      messagebox.showinfo(title = "查無資料", message = "請檢查篩選條件是否正確，\n或 點擊\"搜尋\"尋找新店家!!!", parent = self.win_root) 
    else:
      filted_data.reset_index(inplace = True, drop = True)    #重置索引值
      self.show_random(filted_data)
  
  #顯示隨機美食
  def show_random(self, filted_data):
    rand_num = random.randint(0, filted_data.shape[0] - 1)    #隨機第 num 列
    filted_data = filted_data.loc[rand_num]
    self.txt_name.delete("1.0","end")    # "1.0" 和 "end" 是指第一個字元和最後一個字元
    self.txt_rank.delete("1.0","end")
    self.txt_avgprice.delete("1.0","end")
    self.txt_phone.delete("1.0","end")
    self.txt_opentime.delete("1.0","end")
    self.txt_address.delete("1.0","end")
    self.txt_name.insert("insert", filted_data["Name"])
    self.txt_rank.insert("insert", str(filted_data["Rank"]) + " ★")
    self.txt_avgprice.insert("insert", filted_data["AvgPrice"])
    self.txt_phone.insert("insert", filted_data["Phone"])
    self.txt_opentime.insert("insert", filted_data["OpenTime"])
    self.txt_address.insert("insert", filted_data["Address"])
  
  #建立"搜尋愛食記"的視窗
  def srch_ifoodie(self):
    self.btn_ifoodie.config(state = "disable")
    win_search = Toplevel(self.win_root)
    win_search.title("Searching on Ifoodie.tw")
    win_search.geometry("560x960+1155+30")
    win_search.resizable(0, 0)
    app_search(win_search)
    #關閉搜尋視窗，恢復主視窗的搜尋按鈕
    def win_destroy():    
      self.btn_ifoodie.config(state = "normal")
      win_search.destroy() 
    win_search.protocol('WM_DELETE_WINDOW', win_destroy)    #打叉叉後執行
  
  #是否儲存資料訊息視窗
  def save_msg(self, win_close):
    if win_close:
      Ans = messagebox.askyesno(title = "儲存美食資訊", message = "關閉視窗前是否儲存美食資訊？", parent = self.win_root)
      if Ans:
        Rent.save_database()
      self.win_root.destroy()
    else:
      Rent.save_database()
  
  #顯示作者
  def show_author(self):
    messagebox.showinfo(title = "作者資訊", message = "作者: 陳慶泓（ChingHong）\n信箱: khchen.183@gmail.com", parent = self.win_root)
  
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
    Label(self.frm_opera,  text = "均消:",   **Rent.srch_opt7).place(anchor = "w", x = 60, y = 85)
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
        self.food_data[item[0]]["Phone"] = item[1][0]
        self.var_phone[item[0]].set(self.food_data[item[0]]["Phone"])
        self.img_crawl[item[0]] = ImageTk.PhotoImage(item[1][1])
        self.lb_img[item[0]].config(bg = "#272727", image = self.img_crawl[item[0]])
        self.btn_adds[item[0]].config(state = "normal")
    except:
      Ans = messagebox.askretrycancel(title = "連線異常!!!", message = "是否等待 5 秒後\n重新取得圖片與電話？", icon = "info", parent = self.win_search)
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
        temp = item.find("div", class_ = "avg-price").getText()[5:]
        if temp == "":
          avg_price = "尚無資訊"
        else:
          avg_price = temp
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
      self.food_data[count] = {"Name":title,"Rank":rank,"AvgPrice":avg_price,"OpenTime":open_time,"Address":address,"Category":category}
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
      Label(self.frm_fd[num], text = self.food_data[num]["Name"],     **Rent.srch_info2, bg = color).place(x = 82, y = 8)
      Label(self.frm_fd[num], text = self.food_data[num]["Rank"] + " ★",      **Rent.srch_info4, bg = color).place(x = 250, y = 45)
      Label(self.frm_fd[num], text = self.food_data[num]["AvgPrice"], **Rent.srch_info4, bg = color).place(x = 250, y = 70)
      Label(self.frm_fd[num], text = self.food_data[num]["OpenTime"][:3], **Rent.srch_info4, bg = color).place(x = 250, y = 120)
      Label(self.frm_fd[num], text = self.food_data[num]["Address"],   **Rent.srch_info4, bg = color).place(x = 250, y = 145)
      self.var_phone[num] = StringVar()
      self.var_phone[num].set("請稍後...")
      Label(self.frm_fd[num], textvariable = self.var_phone[num], **Rent.srch_info4, bg = color).place(x = 250, y = 95)
      Label(self.frm_fd[num], bg = color, image = self.img_frame).place(anchor = "center", x = 123, y = 109)
      self.lb_img[num] = Label(self.frm_fd[num], bg = color, image = self.img_waiting)
      self.lb_img[num].place(anchor = "center", x = 125, y = 108)
      #顯示新增按鈕
      self.btn_adds[num] = Button(self.frm_fd[num], activebackground = color, image = self.img_heart, relief = "flat", state = "disable", bg = color)
      self.btn_adds[num].config(command = lambda input = {0:self.food_data[num]}: self.add_to_database(input))
      self.btn_adds[num].place(anchor = "center", x = 20, y = 90)
    self.update_Scrollregion()

  #新增功能按鈕
  def add_to_database(self, data):
    #重新編排字典順序
    rearrange_keys = ["Name","Rank","AvgPrice","Phone","OpenTime","Address","Category"]
    rearrange_data = {}
    for num in data:
      #過濾均消的字元
      filted_chars = ["$","-","以下","以上"]
      try:#重複點擊資料會出錯(原因不明)
        for char in filted_chars:
          data[num]["AvgPrice"] = data[num]["AvgPrice"].replace(char, "")
        if data[num]["AvgPrice"] != "尚無資訊":
          temp_list = list(map(int, data[num]["AvgPrice"].split()))
          temp_avg = int(sum(temp_list)/len(temp_list))
          data[num]["AvgPrice"] = temp_avg
      except:
        pass
        # print(data[num]["AvgPrice"])
      #篩選出縣市、地區的資料
      Address = data[num]["Address"].replace("臺","台")
      c1 = 0
      for s1 in Address:
        c1 += 1
        if s1 == "市":
          temp = Address[c1:]
          c2 = 0
          for s2 in temp:
            c2 += 1
            if s2 == "區":
              break
          break
        if s1 == "縣":
          temp = Address[c1:]
          c2 = 0
          for s2 in temp:
            c2 += 1
            if s2 == "鄉" or s2 == "鎮" or s2 == "市":
              break
          break
      #重新編排字典順序
      rearrange_data[num] = {}
      for key in rearrange_keys:
        if key == "OpenTime" or key == "Category":
          rearrange_data[num][key] = " ".join(data[num][key])
        elif key == "Address":
          rearrange_data[num][key] = Address
        else:
          rearrange_data[num][key] = data[num][key]
      rearrange_data[num]["Area"] = Address[c1-3:c1]
      rearrange_data[num]["SubArea"] = temp[:c2]
    
    #資料轉 DataFrame
    rearrange_data = list(rearrange_data.values())    #打平去掉字典的編號
    pf_data = pd.DataFrame(rearrange_data)
    global EX_database
    EX_database = EX_database.append(pf_data, ignore_index = True)                                            #新增到 DataBase 中
    EX_database.drop_duplicates(subset = ["Address"], keep = "first", inplace = True, ignore_index = True)    #取除重複(地址)資料
    window_root.data_to_treev()
    #更新篩選條件的資料
    Rent.fd_refresh(Is_reset = False)
    window_root.cbb_slcType.config(values = ["不選擇"] + all_Category) 

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
  mp.freeze_support()
  EX_database = pd.read_excel("Database//Cuisine_data.xlsx")
  all_Category = []
  Rent.fd_refresh(Is_reset = True)

  #建立主視窗
  win_root = Tk()
  win_root.iconphoto(True, PhotoImage(file = "Image\\Eating.png"))
  win_root.title("Cuisine Picking")
  win_root.geometry("755x940+400+30")
  win_root.resizable(0, 0)
  window_root = app_main(win_root)
  win_root.mainloop()