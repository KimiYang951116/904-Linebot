from PIL import Image, ImageFont, ImageDraw
import time
local = time.localtime()
fonttype =  'kaiu.TTF'
good = Image.open('Certificate.png')
times= '3'
name = 'Kimi 楊晨諺 108'
drawobj = ImageDraw.Draw(good)
fontinfo = ImageFont.truetype(fonttype, 100)
fontinfo2 = ImageFont.truetype(fonttype, 50)
drawobj.text((910,880),times,fill = 'Black', font = fontinfo)
drawobj.text((870,600),name,fill = 'Black', font = fontinfo)
drawobj.text((800,1100),f'西元{local.tm_year}年{local.tm_mon}月{local.tm_mday}日',fill = 'Black', font = fontinfo2)
good.save('FCertificate.png')