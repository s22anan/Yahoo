import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

# ヤフーニュースのトップページ情報を取得する
URL = "https://news.yahoo.co.jp/topics/top-picks"
res = requests.get(URL)

# BeautifulSoupにヤフーニュースのページ内容を読み込ませる
soup = BeautifulSoup(res.text, "html.parser")

# URLに news.yahoo.co.jp/pickup が含まれるものを抽出する。
data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

#! ここから先を修正、追記 !#

# ヤフーニュース見出のURL情報をループで取得し、リストで格納する。
headline_link_list = [data.attrs["href"] for data in data_list]

newslist=[]
# ヤフーニュース見出のURLリストから記事URLを取得し、記事内容を取得する
for headline_link in headline_link_list:

    # ヤフーニュース見出のURLから、　要約ページの内容を取得する
    summary = requests.get(headline_link)

    # 取得した要約ページをBeautifulSoupで解析できるようにする
    summary_soup = BeautifulSoup(summary.text, "html.parser")

    # aタグの中に「続きを読む」が含まれているテキストを抽出する
    # ヤフーのページ構成は[Top] -> [要約] -> [本文] となっており、
    # [要約]から[本文]に遷移するには「続きを読む」をクリックする必要がある。
    summary_soup_a = summary_soup.select("a:contains('記事全文を読む')")[0]

    # aタグの中の"href="から先のテキストを抽出する。
    # するとヤフーの記事本文のURLを取得できる
    news_body_link = summary_soup_a.attrs["href"]

    # 記事本文のURLから記事本文のページ内容を取得する
    news_body = requests.get(news_body_link)
    # 取得した記事本文のページをBeautifulSoupで解析できるようにする
    news_soup = BeautifulSoup(news_body.text, "html.parser")

    # 記事本文のタイトルを表示する
    print(news_soup.title.text)

    # 記事本文のURLを表示する
    print(news_body_link)

    # class属性の中に「Direct」が含まれる行を抽出する
    detail_text = news_soup.find(class_=re.compile("Direct"))

    # 記事本文を出力する
    # hasattr:指定のオブジェクトが特定の属性を持っているかを確認する
    # detail_text.textの内容がNoneだった場合は、何も表示しないようにしている。
    print(detail_text.text if hasattr(detail_text, "text") else '', end="\n\n\n")
    newslist.append(detail_text)


print(newslist)

df=pd.DataFrame(newslist,columns=['kiji'])
print(df)

df.to_csv("kiji2.csv")