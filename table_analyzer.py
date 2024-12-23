
import fitz
from pprint import pprint
import numpy as np
import pandas as pd
import os

#pdfファイルに含まれる表データを抽出するプログラム
#pdfは「日本中学校体育連盟」の「加盟校調査」（https://nippon-chutairen.or.jp/data/）を例にしています

#pdfを格納しているディレクトリー
dir_path = "./pdf/"
pdf_files = os.listdir(dir_path)

#出力ファイルの列名を設定するためのフラグ
flg = 0

for pdf_file in pdf_files:
   #PDFを開く
   doc = fitz.open(dir_path + pdf_file)
   
   ###ページを指定して、各ページの情報を取得する
   #加盟校（男子）
   #page = doc[2]
   #加盟校（女子）
   #page = doc[3]
   #部員（男子）
   #page = doc[4]
   #部員（女子）
   page = doc[5]
   
   #ページ上にあるテーブルを検出する
   tabs = page.find_tables()
   
   #tabs[0].extract()で表にある全ての行を配列で取得
   #tabs[0].extract()[0]で１行目（列名）を取得できる
   #この表では無駄な改行や空白列を除いて取得する
   columns_list = []
   for r in tabs[0].extract()[0][2:]:
      columns_list.append(r.replace("\n","",10))
   
   #列名を整形
   columns_list = ["row","都道府県"] + columns_list
   
   #年ごとの表記揺れを整形
   columns_list = ["バレーボール" if x == "バレー" else x for x in columns_list]
   columns_list = ["バスケットボール" if x == "バスケット" else x for x in columns_list]
   columns_list = ["バドミントン" if x == "バトミントン" else x for x in columns_list]
   
   #出力ファイルの列名を設定してデータフレームを作成（１回だけ実行）
   if flg == 0:
      df_all = pd.DataFrame(columns=columns_list)
      flg = 1
   
   df_tmp = pd.DataFrame(tabs[0].extract(), columns=columns_list)
   df_tmp = df_tmp.drop([0])
   
   #無駄な行を除去
   df_tmp = df_tmp[df_tmp["都道府県"] != "小計"]
   df_tmp = df_tmp[df_tmp["都道府県"] != "None"]
   df_tmp.dropna(subset=["都道府県"], inplace=True)
   
   #どの年のデータか分かるように年の列を追加
   df_tmp["year"] = pdf_file.replace(".pdf","")
   #出力ファイルに読み込んでいる各表を結合
   df_all = pd.concat([df_all, df_tmp])
   

###完成！！！
print(df_all)

