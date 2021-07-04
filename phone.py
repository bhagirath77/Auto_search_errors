import mechanize
from bs4 import BeautifulSoup

url = "https://www.findandtrace.com/trace-mobile-number-location"

brow = mechanize.Browser()
brow.set_handle_robots(False)

brow.open(url)
brow.select_form(name="trace")
brow['mobilenumber'] = str(input("Enter number: "))

result = brow.submit()

soup = BeautifulSoup(result.read(), 'html.parser')
table_extr = soup.find_all('table',class_ = 'shop_table')
dta = table_extr[0].find('tfoot')
count = 0
for tr in dta:
    count+=1
    if count in (1,4,6,8,10):
        continue
    th = tr.find('th').get_text()
    td = tr.find('td').get_text()
    print(th," : ", td)
dta = table_extr[1].find('tfoot')
cont = 0
for tr in dta:
    cont+=1
    if cont in (2,4,8,10,12,14,16,20,24,26):
        th = tr.find('th').get_text()
        td = tr.find('td').get_text()
        print(th, td)
