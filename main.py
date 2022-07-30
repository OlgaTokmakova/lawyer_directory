import re
import requests
from bs4 import BeautifulSoup
import lxml
import json

url = 'https://www.rechtsanwaelte.at/buergerservice/servicecorner/rechtsanwalt-finden/?tx_rafinden_simplesearch%5Blimit%5D=50&tx_rafinden_simplesearch%5Baction%5D=fullList&tx_rafinden_simplesearch%5Bcontroller%5D=LawyerSearch&cHash=c97b0678c7a3fa2d5365961c15de43aa'


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('index.html', 'w') as file:
#     file.write(src)

# with open('index.html') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# all_lawyer = soup.find_all(href=re.compile("rechtsanwalt-finden"))
#
# all_lawyer_dict = {}
# count = 1
# for item in all_lawyer:
#     print(count)
#     item_text = count
#     item_href = 'https://www.rechtsanwaelte.at' + item.get('href')
#     all_lawyer_dict[item_text] = item_href
#     count += 1
#
# with open('all_lawyer_dict.json', 'w') as file:
#     json.dump(all_lawyer_dict, file, indent=4, ensure_ascii=False)


with open('all_lawyer_dict.json') as file:
    all_lawyer = json.load(file)

count = 0
lawyer_list_result = []
for lawyer_name, lawyer_href in all_lawyer.items():
    count += 1
    print(count)
    print(lawyer_href)
    req = requests.get(url=lawyer_href, headers=headers)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        lawyer_info = soup.find('span', class_='lastname')
        lawyer_fullname = lawyer_info.text

        lawyer_info2 = soup.find('td', id='tm')
        lawyer_address = lawyer_info2.text.strip().split(' ')
        lawyer_address_zip = lawyer_address[0]
        lawyer_address_city = str(lawyer_address[1][0])
        for i in lawyer_address[1][1:]:
            if i not in 'ABСDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ':
                lawyer_address_city += i
            else:
                break
        lawyer_address_street = lawyer_address[1].split(lawyer_address_city)[1] + ' ' + lawyer_address[2]

        lawyer_info3 = soup.find('ul', class_='lawywer-search')
        lawyer_phone = lawyer_info3.find('li').text.strip().split(': ')[1]
        lawyer_mail = lawyer_info3.find('a').text.strip()

        try:
            lawyer_web = lawyer_info3.find('li', target='_blank').text.strip()
        except Exception:
            lawyer_web = 'No website'

        lawyer_list_result.append(
            {
                'Name': lawyer_fullname,
                'Street': lawyer_address_street,
                'ZIP': lawyer_address_zip,
                'City': lawyer_address_city,
                'Phone number': lawyer_phone,
                'Website': lawyer_web,
                'Email': lawyer_mail
            }
        )

    except Exception as ex:
        print(ex)

with open('lawyer_list_result.json', 'a', encoding='utf-8') as file:
    json.dump(lawyer_list_result, file, indent=4, ensure_ascii=False)
