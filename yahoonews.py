from gensim import corpora
from gensim import models
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer

import re
import MeCab
import pandas as pd
import glob

# class Aozoraをimportしたいファイルと同じディレクトリ内に置く
class Game:
    decoration = re.compile(r"(［[^［］]*］)|(《[^《》]*》)|[｜\n]")
    def __init__(self, filename):
        self.filename = filename
        # ワイのははutf-8なので
        with open(filename, "r", encoding="utf-8") as afile:
            self.whole_str = afile.read()
        paragraphs = self.whole_str.splitlines()
        # 最後の3行の空白行以降のコメント行を除く
        c = 0
        position = 0
        for (i, u) in enumerate(reversed(paragraphs)):
            if len(u) != 0:
                c = 0
            else:
                c += 1
                if c >= 3:
                    position = i
                    break
        if position != 0:
            paragraphs = paragraphs[:-(position+1)]
 
        # 先頭の----行で囲まれたコメント領域の行を除く
        newparagraphs = []
        addswitch = True
        for u in paragraphs:
            if u[:2] != '--':
                if addswitch:
                    newparagraphs.append(u)
            else:
                addswitch = not addswitch
 
        self.cleanedparagraphs = []
        for u in newparagraphs:
            v = re.sub(self.decoration, '', u)
            self.cleanedparagraphs.append(v)
 
    def read(self):
        return self.cleanedparagraphs



aozoradir = "./"
m = MeCab.Tagger("-Owakati")  # MeCabで分かち書きにする
dir = '/Users/nakagomeyuusuke/yahoo/'
files = glob.glob(dir+'*.txt')

#files = ['./rocket.txt', './ARK.txt', './peach beach splash.txt', './Papers,Please.txt', './Fallguys.txt', './鉄拳.txt',
 #'./syutage.txt', './ATRI.txt', './fallout.txt', './アズールレーン.txt', './hitman.txt', './DBD.txt', './ダンガンロンパV3.txt', 
 #'./ストファイ.txt', './RUST.txt', './cookingsimulator.txt', './アンダーテール.txt', './ニーアオートマタ.txt', './神田川ジェットガール.txt', './SEKIRO.txt', 
 #'./シージ.txt', './speed runner.txt', './PUBG.txt', './ペル4.txt', './golf with your friends.txt', './モンハン.txt', './聖剣伝説３.txt', 
 #'./夜勤事件.txt', './ダンガンロンパ.txt', './グラブルバーサス.txt', './project winter.txt', './ダークソウル.txt', './ですスト.txt', './FF15.txt', 
 #'./ドキドキ文芸部.txt', './ultimate.txt', './ライザのアトリエ.txt', './shinobi vursus.txt', './GTA5.txt', './red.txt', './仁王.txt']
#readtextlist = [Game(aozoradir + u) for u in files]
readtextlist = [Game(u) for u in files]
stringlist = ['\n'.join(u.read()) for u in readtextlist]
stringlist[2]
#print(files)

import MeCab

# ストップワードリスト 入れたくない言葉をここに入れる
stopwords=['いる', 'する', 'よう', 'の', 'なる', 'ん', 'ある', 
           'それ', '方', 'れる', 'こと', 'とき', 'たち', 'そう',
           'もの', 'そこ', 'さっき', 'こっち', 'とこ', 'られる', 
           'てる', 'ここ', 'そっち', 'ら', 'どこか', 'そこら', 
           'あれ', 'どれ', 'これ', 'さ', 'せる', 'く', 'ぁ', 
           'あっち', 'どっち', 'べる。', 'ぃん','。','®','▪','　','-','&','))','!!',
          '[/',']：','2018','3','MISS','10','®。','1997',
          'REMAKE','9','12','25','11','OB','やる','Miss','Mr',
          '1080','22','7','R','1','8','CRT','VHS','b','40','Xbox',
          'Rocket','League','Cars','one','Battle','Powered']
wakatilist=[]
for txt in stringlist:
#    txt.encode('utf-8')
    m=MeCab.Tagger()
    m.parse('')
    node=m.parseToNode(txt)
    
    doc=''
    while node:
        if node.feature.split(',')[6] == '*': # 原形を取り出す
            term=node.surface
        else :
            term=node.feature.split(',')[6]
        
        if term in stopwords:
            node=node.next
            continue
    
        if node.feature.split(',')[0] in ['名詞', '動詞', '形容詞']:
            doc=doc+' '+term
#        print(term)
        
        node=node.next
        
    wakatilist.append(doc)

    # norm=Noneでベクトルの正規化（長さを1にする）をやめる
vectorizer = TfidfVectorizer(use_idf=True, norm=None, token_pattern=u'(?u)\\b\\w+\\b')
tfidf = vectorizer.fit_transform(wakatilist)

tfidfpd = pd.DataFrame(tfidf.toarray())     # pandasのデータフレームに変換する

itemlist = sorted(vectorizer.vocabulary_.items(), key=lambda x:x[1])
tfidfpd.columns = [u[0] for u in itemlist]  # 欄の見出し（単語）を付ける

import numpy as np

def comp_sim(qvec,tvec):
    return np.dot(qvec.T, tvec)[0][0] / (np.linalg.norm(qvec) * np.linalg.norm(tvec))

X=0
y=0
Y=int(X-1)
Gazou=[]
cos = []
Ans=[]
for g in range(80):
    Y = int(Y+1)

    for i in range(80):
        y = i
        ans=comp_sim(tfidfpd.iloc[Y,:].to_numpy().reshape(-1,1),tfidfpd.iloc[y,:].to_numpy().reshape(-1,1))
        Ans.append(ans) 
        cos.append(ans)
        print(ans,files[i])
        #print(Ans)
        #print(sorted(ans,key=lambda x:x[0], reverse=True))
        #print(sorted(ans,key=float, reverse=True))
        #result = sorted(Ans,key=lambda x:x[0])
        #print(ans)

