# -*- coding: utf-8 -*-

class StockList():
    def __init__(self):
        pass

    def get_all_stock_list(self):
        pass

def get_stock_list(lst, stock_url):
    html = getHTMLText(stock_url, "GB2312")
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue


def get_stock_info(lst, stock_url, file_path):
    count = 0
    for stock in lst:
        url = stock_url + stock + '.html'
        html = getHTMLText(url)
        try:
            print('get stock info')
            if html == "":
                continue
            info_dict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stock_info = soup.find('div', attrs={"class":"stock-bets"})

            name = stock_info.find_all(attrs={"class":"bets-name"})[0]
            info_dict.update({'股票名称': name.text.split()[0]})

            key_list = stock_info.find_all('dt')
            value_list = stock_info.find_all('dd')

            for i in range(len(key_list)):
                key = key_list[i].text
                val = value_list[i].text
                info_dict[key] = val

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(str(info_dict) + '\n')
                count += 1
                print("\r当前进度：{:.2f}%".format(count*100/len(lst)), end="")
        except:
            count += 1
            print("\r当前进度：{:.2f}%".format(count * 100 / len(lst)), end="")
            continue

