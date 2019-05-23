from django.test import TestCase

# Create your tests here.




from PIL import Image,ImageFont,ImageDraw
from PIL import Image

im = Image.open('../ava.png')
im2 = Image.open('../xcx.jpg')


huabu_x = 375   # 画布宽度
huabu_y = 550   # 画布高度

# 新建画布纯白色           宽度↓   ↓高度    ↓ 颜色
p = Image.new('RGBA', (huabu_x, huabu_y) , (255, 255, 255))

qr_suofang_x = 114  # 固定小程序二维码 宽度
qr_suofang_y = 114  # 固定小程序二维码 高度

# 缩放图片 小程序二维码
im2 = im2.resize((qr_suofang_x, qr_suofang_y))

qr_x = huabu_x - (qr_suofang_x + 45) # 小程序二维码 距右侧 减去 (本身宽度 + 45px)
qr_y = huabu_y - (qr_suofang_y + 30) # 小程序二维码 距右侧 减去 (本身宽度 + 30px)

p.paste(im2, (qr_x, qr_y))          # 把缩放的小程序二维码 放到画布上

im = im.resize((huabu_x, (qr_y - 20))) # 缩放封面 宽度同画布宽度一样 高度为 小程序二维码高度 减去20

p.paste(im, (0,0))  # 把缩放的 封面 放到画布

font = ImageFont.truetype('/usr/share/fonts/chinese/simsun.ttc', 18)

image_draw = ImageDraw.Draw(p)

text = '长按识别图中二维码\n\n 查看她的变美过程'

image_draw.text((25, huabu_y-qr_suofang_y), text, font=font, fill=(0, 0, 0))

p.save('../1.png')










