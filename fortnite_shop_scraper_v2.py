import requests
import os
from PIL import Image,ImageDraw, ImageFont
from io import BytesIO
import os
import shutil


# APIのURL
url = "https://fortnite-api.com/v2/shop?language=ja"


# リクエストの送信とJSONの解析
response = requests.get(url)
data = response.json()

#ディレクトリ内のアイテム全削除
shutil.rmtree('fortnite_items/')
# 画像保存用のディレクトリ作成
if not os.path.exists('fortnite_items'):
    os.makedirs('fortnite_items')

# アイテムの情報を取得し、画像をダウンロード
for entry in data['data']['entries'] :
    #print(entry)
    price = entry['finalPrice']
    if 'brItems' in entry:
        #バンドルの場合
        if 'bundle' in entry:
            name = entry['bundle']['name']
            image_url =entry['bundle']['image']
        else:
            name = entry['brItems'][0]['name']
            if 'featured' in entry['brItems'][0]['images']:
                image_url = entry['brItems'][0]['images']['featured']
            else:
                image_url = entry['brItems'][0]['images']['icon']
        print(name + " " + str(price)+"V")
        print(image_url)
    
        
        # 画像のダウンロードと保存
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content)).convert("RGBA")
        w =img.width
        if w < 1024 :
            img  = img.resize((1024,1024),Image.Resampling.LANCZOS)
        
        #背景画像
        img_bg = Image.open("Background.png").convert("RGBA")
        
        #合成
        im2 =img_bg.copy()
        im2.paste(img,(0,0),img)
        
        #画像にテキスト追加
        draw = ImageDraw.Draw(im2)
        font = ImageFont.truetype("Corporate-Logo-Rounded-Bold-ver3.otf", 60)
        
        draw.rectangle((0,800,1024,1024),fill=(0,0,0))
        draw.text((100, 950), name +"\n" + str(price)+"V-BUCKS", font=font, anchor='ld', fill='white') 
        
       
        # ファイル名の作成（スペースをアンダースコアに置換）
        filename = f"{name.replace(' ', '_')}_{price}.png"
        
        # 画像の保存
        im2.save(os.path.join('fortnite_items', filename))
        
    #print(f"保存しました: {filename}")

print("完了しました！")