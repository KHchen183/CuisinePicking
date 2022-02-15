import requests as req
import bs4

def crawl_top15(Fd_type, Area, Sort_by):
  Area = "" if Area == "-" else "/" + Area
  Fd_type = "" if Fd_type == "-" else "/" + Fd_type
  Sort_by = "" if Sort_by == "-" else "?sortby=" + Sort_by
  src = "https://ifoodie.tw/explore" + Area +"/list" + Fd_type + Sort_by

  req_data = req.get(src).text
  entire_data = bs4.BeautifulSoup(req_data, "html.parser")
  items = entire_data.find_all("div", class_ = "restaurant-info")
  #上下頁網址
  try:
    nextlink = "https://ifoodie.tw" + entire_data.find("a", string="下一頁 ›")["href"]    #下一頁網址
  except:
    nextlink = "no next page"
  try:
    prevlink = "https://ifoodie.tw" + entire_data.find("a", string="上一頁")["href"]      #上一頁網址
  except:
    prevlink = "no pre page"
  #店家資訊
  for item in items:
    get_title = item.find("a", class_ = "title-text")
    detail_scr = "https://ifoodie.tw" + get_title["href"]                                    #取得該店家詳細資訊的網址
    title = get_title.getText()                                                              #店家名稱
    rank = item.find("div", class_ = "text").getText()                                       #評價
    address = item.find("div", class_ = "address-row").getText()                             #地址
    open_time = item.find("div", class_ = "info").getText()                                  #營業時間
    avg_price = item.find("div", class_ = "avg-price").getText().replace("· 均消 ", "")      #均消
    print(title, rank, address, open_time, avg_price, sep = "\n")
    #圖片資訊
    try:
      img_url = item.a.img
      if img_url.has_attr("data-src"):    #"has_attr("")":判斷屬性是否存在
        img_url = img_url["data-src"]
      else:
        img_url = img_url["src"]   
    except:
      img_url = "Wrong"
    
    categorys = item.find("div", class_ = "category-row").find_all("a", class_ = "category")
    for category in categorys:
      print(category.getText())
    print("---------------------------------------")

  return detail_scr
  #備註：.string 與 .getText()功能相似；.getText() = .get_text() = .text

Area = "台中市"
Fd_type = "火鍋"
Sort_by = "rating"

detail_scr = crawl_top15(Fd_type, Area, Sort_by)

#訪問詳細的新網址
# detail_response = req.get(detail_scr).text                   
# detail_data = bs4.BeautifulSoup(detail_response, "html.parser").find("div", class_ = "main-content")
# phone = detail_data.find("div", class_ = "phone-wrapper").find("span", class_ = "detail").a.getText()
# img_url = detail_data.find("img", class_ = "cover")["src"]
# print(phone, img_url, sep = "\n")
