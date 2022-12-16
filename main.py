import requests
from  bs4 import BeautifulSoup
import time
import csv
import random
from pyfiglet import Figlet
import json
from collections import Counter
from collections import OrderedDict

resultlist = []

headers = {'useragent1':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'

}


def namejson():
    tym = time.localtime()
    opt = time.strftime("%d.%b.%Y",tym)
    objectname = 'RGD_synth.' + opt + '.json'
    return objectname


def namejson2():
    tym = time.localtime()
    opt = time.strftime("%d.%b.%Y",tym)
    objectname = 'RGD_.' + opt + '.json'
    return objectname


def html(url):
    r = requests.get(url, headers=headers)
    return r.text


def data(r):
    g = int(input('Режим отладки 1, ручной ввод 2: '))
    soup = BeautifulSoup(r, 'lxml')
    data = soup.find('div', id='b2').find('span', id='port_body').find('ul')
    invcorp = data.find_all('li')
    all1 = len(invcorp)
    if g == 2:
        iter1 = int(input(f'Сколько проанализировать фондов до ({all1}) ?: '))
        allinfo = int(input('Вывод всех значений [1]: '))
        if allinfo != 1:
            value1 = float(input(f'Введите желаемую цену за акцию: '))
            iter2 = float(input('Введите желаемое падение или рост акции \n(Рекомендовано: -5): '))
        else:
            value1 = float(80)
            iter2 = float(-5)
    else:
        allinfo = int(input('Вывод всех значений [1]: '))
        if allinfo != 1:
            value1 = float(80)
            iter2 = float(-5)
            iter1 = int(4)
        else:
            value1 = float(80)
            iter2 = float(-5)
            iter1 = int(4)
    i = 0
    linkss = []
    i1 = 1
    for datas in invcorp:
        url = 'https://www.dataroma.com'
        named = datas.find('a')
        links = url + named.get('href')
        date = named.find('span').text
        print(named.text)
        print(f'{i1}. {links}')
        linkss.append(links)
        print(date.strip('')[9:])
        print('-----------------------------------------------------------------')
        i += 1
        i1 += 1
        if i == int(iter1):
            print('\n')
            print(f'Поиск от ${value1} и менее.'
                  f'\nВы ввели: [{iter1}] для колличества компаний.'
                  f'\nПоиск от {iter2}% и более.')
            print('\n')
            datacompurl(linkss,iter2,value1,allinfo)
            break



def datacomp(r,numname,iter2,value1,allinfo):
    soup = BeautifulSoup(r, 'lxml')
    data = soup.find(id = 'wrap').find_all('tr')
    name = soup.find('div',id = 'f_name').text.split('\n')[0]
    print(f'{numname}. {name}')
    # dictall(name)
    print('-----------------------------------------------------------------')
    i = 1
    for datas in data:
        try:
            url = 'https://www.dataroma.com'
            pr = datas.find_all('td')[2].text + '%'
            named = datas.find(class_ ="stock").find('span').text
            ticker = datas.find(class_="stock").text.split()[0]
            links = url + datas.find(class_ ="stock").find('a').get('href')
            what = datas.find_all('td')[3].text
            price = datas.find(class_ ="quote").text
            reported = datas.find_all('td')[9].text
            pri = float(price.replace('$', ''))
            rep = float(reported.replace('%',''))
            # print(what.find() == True)
            # or what.find('Buy') == 0 or what.find('Add') == 0
            if allinfo == 1:
                print(
                    f'{i}. {pr.rjust(6, " ")},{str(ticker[0:5])}{named[0:10]} {price} ({what[0:14]}) : {reported.rjust(6, " ")} url = {links}')
                i += 1
                namedict = 'dict' + str(numname)
                namedict = [{
                    '%': pr,
                    'ticker': ticker,
                    'price': price,
                    'what': what,
                    'reported': reported,
                    'links': links
                }]
                writejson(namedict, namejson())
                dictsynth1(namedict)
            elif pri <= value1 and rep <= iter2:
                if len(what) == 1:
                    what = ('Поз. до обнов')
                    print(
                        f'{i}. {pr.rjust(6, " ")},{str(ticker[0:5])}{named[0:10]} {price} ({what[0:14]}) : {reported.rjust(6, " ")} url = {links}')
                elif len(what) == 4:
                    what = ('      Buy    ')
                    print(
                        f'{i}. {pr.rjust(6, " ")},{str(ticker[0:5])}{named[0:10]} {price} ({what[0:14]}) : {reported.rjust(6, " ")} url = {links}')
                elif len(what) == 12:
                    print(
                        f'{i}. {pr.rjust(6, " ")},{str(ticker[0:5])}{named[0:10]} {price} ({what[0:14]} ) : {reported.rjust(6, " ")} url = {links}')
                else:
                    print(f'{i}. {pr.rjust(6, " ")},{str(ticker[0:5])}{named[0:10]} {price} ({what[0:14]}) : {reported.rjust(6, " ")} url = {links}')
                i += 1
                namedict = 'dict' + str(numname)

                namedict = [{
                        '%':pr,
                        'ticker':str(ticker),
                        'price':price,
                        'what':what,
                        'reported':reported,
                        'links': links
                        }]


                writejson(namedict,namejson())
                dictsynth1(namedict)

                # print(f'{i}. {pr}{named} {price} ({what.strip()}) : {reported} url = {links}')

                # print(f'{i}. {pr}{named} {price} ({what.strip()}) : {reported} url = {links}')
            # elif price.split('$')[1] <= value1 and what.find('Add') == 0 or what.find('Buy') == 0 or reported.strip('%') <= str(iter2) or what.find('Reduce') == 0:
            #     print(f'{i}. {pr}{named} {price} ({what.strip()}) : {reported} url = {links}')


        except Exception as e:
            # print(e)
            continue


# def dictall(name,i, pr, ticker):
#
#     # name = name.append
#     # i = i.append
#     # pr = pr.append
#
#     dict = {'name': name.append(name)
#        [
#         {'№':i.append(i),
#          '%':pr.append(pr),
#          'ticker':ticker.append(ticker)}
#         ]
#             }
#     print(dict)

def synth(objectname):
    # print(resultlist)
    # searchtick = Counter(x["ticker"]+ ' - ' + x["price"] + ' - ' + x["reported"] + ' - ' + x["links"] for x, in resultlist).most_common(5)
    # sort = input('Сортировать по колличеству')
    searchtick = Counter(x["ticker"]+ ' - ' + x["price"] + ' - ' + x["reported"] for x in resultlist).most_common(15)
    searchurl = Counter(x["links"] for x in resultlist).most_common(15)
    list3 = []
    for i in range(len(searchurl)):
        g = searchurl[i][0]
        list3.append(g)

    list2 = []
    for i in range(len(searchurl)):
        g = searchurl[i][1]
        list2.append(g)

    gff = dict(zip(list3,list2))

    print(searchtick)
    # # g = list(searchtick.items())
    # # print(type(g))
    # # result = g
    # data1 = json.dumps(searchtick)
    # data2 = json.loads(data1)
    # # print(searchtick,'\n',searchurl)
    # # print(result)
    # # print(f'{searchtick} \n{searchurl}')
    # # data1 = [searchtick]
    # print(data1)
    # print(data2)
    finaljson(searchtick,gff, namejson2())


    # re = input(str('Провести сортировку ? '))
    # if re == 1:
    #     with open (objectname) as f:
    #         data = json.load(f)
    #     print(data)
    #     for section, comands in data.items():
    #         print(section)
    #         print('\n'.join(comands))
    # else:
    #     with open(objectname) as f:
    #         # fc = f.read()
    #         data = json.load(f)
    #         # data = json.dumps(data, indent=4,  ensure_ascii = False)
        # cots = dict()
        # for datas in data:
        #     if datas['ticker'] not in cots.keys():
        #         cots[datas['ticker']] = 1
        #     else:
        #         cots[datas['ticker']] += 1
        # for cot, count in cots.items():
        #     print(f'{cot}:{count}')

            # yourlist = json.dumps(data, indent=4,  ensure_ascii = False, sort_keys=True)

        # for section, comands in data.items():
        #     print(section)
        #     print('\n'.join(comands))

def finaljson(data1,data2,name):
    name = 'Final_' + name
    data1 = data1 , data2
    # try:
    #     data = json.load(open(name))
    # except:
    #     data = []
    # print(type(counter))
    # data.update(counter)
    # data.append(counter2)
    with open('final.txt','w') as f:
        f.write(str(data1))
        f.write(str(data2))


    try:
        data = json.load(open(name))
    except:
        data = []
    # # json.dump(counter,f, indent=1)
    # print(type(counter))
    data.append(data1)
    with open(name, 'w') as file:
        json.dump(data,file, indent=4)
    # json.dump(data2,file, indent=4)
# print(data1)




def datacompurl(linkss,iter2,value1,allinfo):
    numname = 1
    i = len(linkss)
    i -= 0

    while i != 0:
        for i in range(0,i):
            print(datacomp(html(linkss[i]),numname,iter2,value1,allinfo))
            numname += 1
            print('-----------------------------------------------------------------')
            i -= 1
        break
    synth(namejson())
    # sortdict()

def main():
    preview = Figlet(font='isometric1')
    print(preview.renderText('RUSGO\n SOFT'))
    url = 'https://www.dataroma.com/m/home.php'
    data(html(url))



def dictsynth1(list):
    for d in list:
        resultlist.append(d)
        return resultlist


#Запись в txt.
# def dictsynth(dict): №
#     with open('text.txt', 'a') as file:
#         for item in dict:
#             # 2.2.1. Сформировать строку вида key:value
#             s = str(item)  # взять ключ как строку
#             s += ':'  # добавить символ ':'
#             s += dict.get(item)  # добавить значение value по его ключу
#             s += '\n'  # добавить символ новой строки
#
#             # 2.2.2. Записать строку в файл
#             file.write(s)

# def sortdict():
#     with open ('text.txt','r') as f:
#         for k,v in f:
#             print("{0}: {1}".format(k,v))
#             # print(line)



def writejson(dict,name):
    links = 1
    for i in range(links):
        try:
            data = json.load(open(name))
        except:
            data = []
        data.append(dict)
        with open (name, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii = False)



if __name__ == '__main__':
    main()
