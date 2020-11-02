# config: UTF-8
import csv
import logging


async def getUrlList():
    urls = []
    try:
        with open("list.txt", "rb") as f:
            items = f.read()
            urls = items.decode('utf-8').split()
        if urls == []:
            logging.error(u'urls is none')
            logging.error(u'plz write list.txt to url for download target')
            exit()
    except Exception:
        logging.error(u'list.txt is none')
        exit()
    return urls


async def getCsvConfig():
    psdlist = []
    try:
        with open("some.csv", "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                dictmp = {}
                for index, col in enumerate(header):
                    dictmp[col] = row[index]
                psdlist.append(dictmp)
        if psdlist is None:
            logging.error(u'some.csv read error')
            exit()
    except Exception:
        logging.error(u'some.csv is none')
        exit()
    return psdlist
