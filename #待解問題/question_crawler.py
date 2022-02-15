import requests as req
import bs4

src = "https://ifoodie.tw/restaurant/56a2f7422756dd19a5f95754-田樂公正小巷店"
response = req.get(src).text
req_data = bs4.BeautifulSoup(response, "html.parser")

get_open_data = req_data.find("div", class_ = "openingHourWrapper")

#營業時間
open_time = get_open_data.find("div", class_ = "open-text").getText()
print(open_time)
#星期一的營業時間
open_Monday = get_open_data.find("div", class_ = "jss480 weekday-hours today")
print(open_Monday)