# config: UTF-8
import wx
import csv

app = wx.App()


async def getUrlList():
    urls = []
    try:
        with open("list.txt", "rb") as f:
            items = f.read()
            urls = items.decode('utf-8').split()
        if urls is None:
            wx.MessageBox(u'urls is none')
            exit()
    except Exception:
        wx.MessageBox(u'list.txt is none')
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
            wx.MessageBox(u'some.csv read error')
            exit()
    except Exception:
        wx.MessageBox(u'some.csv is none')
        exit()
    return psdlist
