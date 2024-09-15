# pipの保存 pip freeze > requirements.txt
# pipの復元 pip install -r requirements.txt
# OS操作, 中でPillowを使うのでモジュールはインストールしておく。
import configparser
import pyautogui
# 画像操作
from PIL import ImageDraw, ImageFont
# 枚数管理
import os
# lpr実行用
import subprocess

#
# config読込
#
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

# ファイル番号の初期値
Page0 = 10000

# Zoomのトリミング領域　背景画像は　16：9 => 1.78
xo = int(config_ini['CROP']['x0'])
yo = int(config_ini['CROP']['y0'])
wo = int(config_ini['CROP']['w0'])
ho = int(config_ini['CROP']['h0'])


def filename(nn):
    fn = "img/%05d.png" % nn
    return fn


def shot(nn):
    # 画像ポイント
    [xc0, yc0] = [xo + wo / 2, yo + ho / 2]

    # 切り取り位置
    [w, h] = [ho * 1.41, ho]
    [x0, y0] = [xc0 - w / 2, yc0 - h / 2]
    [x1, y1] = [xc0 + w / 2, yc0 + h / 2]
    [cx0, cy0] = [w * 0.05, h * 0.07]  # 文字表示位置

    # スクショ
    src_img = pyautogui.screenshot()

    # 切り取り
    dst_img = src_img.crop((x0, y0, x1, y1))

    # 文字
    font = ImageFont.truetype('ipaexm.ttf', 60)
    draw = ImageDraw.Draw(dst_img)
    fcolor = (255, 255, 255)
    draw.text((cx0, cy0), "2024-09-23 極地研究所一般公開", font=font, stroke_width=2, fill=fcolor)

    # 画像出力
    fn = filename(nn)
    dst_img.save(fn)


def get_pages():
    f = open("shot.txt", "r")
    nn = f.readline()
    f.close()
    return int(nn)


def set_pages(nn):
    f = open("shot.txt", "w")
    f.write(str(nn))
    f.close()
    return


def init_pages():
    if not os.path.isfile("shot.txt"):
        f = open("shot.txt", "w")
        f.write(str(Page0))
        f.close()


def img_print(nn):
    # プリントアウト
    fn = filename(nn)
    cmd = 'lpr %s  -o PageSize=Postcard' % fn
    print(cmd)
    subprocess.call(cmd, shell=True)


def main():
    init_pages()
    while True:
        print("撮影:RET/前の画像プリント:1+RET/終了 q+RET")
        val = input()
        if val == '':
            nn = get_pages()
            shot(nn)
            # img_print(nn)
            print("Print %d" % nn)
            nn += 1
            set_pages(nn)
        elif val == '1' or val == '2' or val == '3':
            nn = get_pages() - int(val)
            if nn >= Page0:
                img_print(nn)
            else:
                print("Invalid page")
            continue
        elif val == 'q':
            break
        else:
            continue


if __name__ == '__main__':
    main()
