import cv2
import numpy as np
import os
import glob
import math
from PIL import Image

def create_adaptive_image_grid(input_dir, output_file, max_cols=None):
    # 指定されたディレクトリから画像ファイルを取得
    image_files = glob.glob(os.path.join(input_dir, '*.*'))
    total_images = len(image_files)
    
    # 最適なグリッドサイズを計算
    if max_cols:
        cols = min(max_cols, total_images)
    else:
        cols = int(math.sqrt(total_images))
    
    rows = math.ceil(total_images / cols)
    
    # グリッドサイズの最適化（より正方形に近づける）
    while rows > 1 and rows * (cols - 1) >= total_images:
        cols -= 1
        rows = math.ceil(total_images / cols)
    
    # 画像を読み込み、リサイズする
    images = []
    for file in image_files:
        img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if img is not None:
            # アルファチャンネルがある場合は処理する
            if img.shape[-1] == 4:
                # アルファチャンネルを使って背景色とブレンド
                alpha = img[:, :, 3] / 255.0
                img_rgb = img[:, :, :3]
                bg_color = np.array([255, 255, 255])  # 白背景
                img_rgb = (alpha[:, :, np.newaxis] * img_rgb + (1 - alpha[:, :, np.newaxis]) * bg_color).astype(np.uint8)
            else:
                img_rgb = img[:, :, :3]
            
            # 画像を512x512にリサイズ
            img_resized = cv2.resize(img_rgb, (512, 512))
            images.append(img_resized)
    
    # グリッドを作成
    grid = np.zeros((rows * 512, cols * 512, 3), dtype=np.uint8)
    
    # 画像をグリッドに配置
    for i, img in enumerate(images):
        if i >= total_images:
            break
        row = i // cols
        col = i % cols
        grid[row*512:(row+1)*512, col*512:(col+1)*512] = img
    
    # 結果を保存
    cv2.imwrite(output_file, grid)
    print(f"画像グリッドを {output_file} に保存しました。")
    print(f"グリッドサイズ: {rows}行 x {cols}列")

# スクリプトの使用例
input_directory = 'fortnite_items/'  # 画像があるディレクトリのパス
output_file = 'output_adaptive_grid.jpg'  # 出力ファイル名
create_adaptive_image_grid(input_directory, output_file)
#画像の圧縮
compressed_image = Image.open(output_file)
compressed_image.save("comp_"+output_file,optimize=True,quality=85)
# オプション: 最大列数を指定する場合
# create_adaptive_image_grid(input_directory, output_file, max_cols=5)