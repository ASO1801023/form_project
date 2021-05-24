from django.shortcuts import render
from .forms import UserForm
from .forms import HikaruForm

# hikaruSys sta
from janome.tokenizer import Tokenizer
import requests
from bs4 import BeautifulSoup
import codecs
import jaconv

from collections import Counter
import random
import pandas as pd
# hikaruSys end

from user.models import Publisher
from user.models import IdeaTree
from user.models import Element

# 漢字をひらがな start
from pykakasi import kakasi
# 漢字をひらがな end

def hikaruSys(request):
    params = {'ans': '', 'form': None}

    if request.method == 'POST': # フォームで送信した時

        if 'button_2' in request.POST:
            kothira()
            params['form'] = HikaruForm()
            return render(request, 'user/hikaruPage.html', params)


        form = HikaruForm(request.POST) #フォームの型を形成(個数とバリデーション)

        firstInput = request.POST['ans']

        ruyWords = ruySystem(firstInput)

        params['input'] = firstInput
        params['ruy1'] = ruyWords[0]
        params['ruy2'] = ruyWords[1]
        params['ruy3'] = ruyWords[2]

        siriWords = siritoriSystem(firstInput)

        params['sir1'] = siriWords[0]
        params['sir2'] = siriWords[1]
        params['sir3'] = siriWords[2]

        params['form'] = form

        insertElement(params) #DB 登録
        
    else: #ただ開いた時
        params['form'] = HikaruForm()

    params['select'] = Element.objects.values('name')

    return render(request, 'user/hikaruPage.html', params)

def insertElement(acc):
    #Element(name=acc['input'], color="0", foreigens="1").save()
    Element(name=acc['ruy1'], path="1", color="2", ideatree_id="1").save()
    #Element(name=acc['ruy2'], foreigens="1").save()
    #Element(name=acc['ruy3'], foreigens="1").save()
    #Element(name=acc['sir1'], foreigens="1").save()
    #Element(name=acc['sir2'], foreigens="1").save()
    #Element(name=acc['sir3'], foreigens="1").save()
    return

def kothira(request): #『こちら』ボタン
    Publisher(name="江崎光").save()
    IdeaTree(name="初めてのツリー",overview="説明",complete_flag="0",idea_theme="林檎",lastidea_id="0",user="1").save()
    return


def ruySystem(acc): #類義語システム
    retData = [0] * 3
    link = "https://ja.wikipedia.org/wiki/"

    keyword = [acc]
    corpus = []
    wordslist = []
    t = Tokenizer()

    for word in keyword:
        with requests.get(link + word) as response: 
            # responseはhtmlのformatになっている
            html = response.text #ページリンク(str)を変数に
            soup = BeautifulSoup(html, "lxml")
            # <p>タグを取得
            p_tags = soup.find_all('p')
            for p in p_tags:
                tokens = t.tokenize(p.text)
                for token in tokens:
                    word = ''
                    if (token.part_of_speech.split(',')[0] in ['代名詞', '名詞', '固有名詞', '動詞', '形容詞', '形容動詞']) and \
                        (token.part_of_speech.split(',')[1] not in ['数','自立', 'サ変接続', '非自立', '接尾', '副詞可能']) and \
                        (token.base_form not in ['これら', 'せる', 'これ']):
                                word = token.base_form
                                wordslist.append(word)
            corpus.append(wordslist)

    responseBox = Counter(corpus[0]) # 取得した単語を全取得
    ansLength = len(responseBox) # 取得した単語の数(int)

    if ansLength > 20: # 20より多いなら
        adapter = responseBox.most_common(20) #出現回数上位20取得
        ansLength = 25 # 
    else : 
        adapter = responseBox.most_common(ansLength) #出現回数全取得

    if ansLength <= 1: # 単語が一つもヒットしなかったら...
        retData = ['Dummy', 'Dummy', 'Dummy']
    else :
        randomClum = random.randrange(ansLength) # ランダム生成

        adapter = responseBox.most_common()
        if ansLength > 3:
            retData = [adapter[randomClum][0], adapter[randomClum-1][0], adapter[randomClum-2][0]]
        elif ansLength == 3:
            retData = [adapter[1][0], adapter[2][0], 'Dummy']
        elif ansLength == 2:
            retData = [adapter[1][0], 'Dummy', 'Dummy']
    
    return retData
    
    

def siritoriSystem(acc): #しりとりシステム
    retData = [0] * 3
    # しりとりサイド
    df = pd.read_csv('japanese.csv')

    # オブジェクトをインスタンス化
    kakasir = kakasi()
    # モードの設定：J(Kanji) to H(Hiragana)
    kakasir.setMode('J', 'H')
    # 変換して出力
    conv = kakasir.getConverter()
    secInput = conv.do(acc)  # => ひらがな化

    sss = df[df['あー'].str.startswith( secInput[-1] )]
    ddd = sss[~(sss['あー'].str.endswith('ん'))]
    if (len(ddd) < 3):
        retData[0] = 'dummy'
        retData[1] = 'dummy'
        retData[2] = 'dummy'
    else :
        stt = ddd.sample(n=3).values.tolist()
        retData[0] = stt[0][0]
        retData[1] = stt[1][0]
        retData[2] = stt[2][0]
    
    return retData


# 初期

def new(request):
    params = {'name': '', 'email': '', 'form': None}
    if request.method == 'POST': # フォームで送信した時
        form = UserForm(request.POST)
        params['name'] = request.POST['name']
        params['email'] = request.POST['email']
        params['form'] = form
    else: #ただ開いた時
        params['form'] = UserForm()
    return render(request, 'user/new.html', params)

def newBack(request):
    params = {'message': 'newです'}
    return render(request, 'user/new.html', params)

