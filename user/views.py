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

# 漢字をひらがな
from pykakasi import kakasi
# 漢字をひらがな
 
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

def hikaruSys(request):
    params = {'ans': '', 'form': None}

    if request.method == 'POST': # フォームで送信した時

        form = HikaruForm(request.POST) #フォームの型を形成(個数とバリデーション)

        link = "https://ja.wikipedia.org/wiki/"
        firstInput = request.POST['ans']
        keyword = [firstInput]
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

        params['ruy1'] = retData[0]
        params['ruy2'] = retData[1]
        params['ruy3'] = retData[2]
        
        # しりとりサイド
        df = pd.read_csv('japanese.csv')

        # オブジェクトをインスタンス化
        kakasir = kakasi()
        # モードの設定：J(Kanji) to H(Hiragana)
        kakasir.setMode('J', 'H')
        # 変換して出力
        conv = kakasir.getConverter()
        secInput = conv.do(firstInput)  # => ひらがな化

        sss = df[df['あー'].str.startswith( secInput[-1] )]
        ddd = sss[~(sss['あー'].str.endswith('ん'))]
        if (len(ddd) < 3):
            params['sir1'] = 'dummy'
            params['sir2'] = 'dummy'
            params['sir3'] = 'dummy'
        else :
            stt = ddd.sample(n=3).values.tolist()
            params['sir1'] = stt[0][0]
            params['sir2'] = stt[1][0]
            params['sir3'] = stt[2][0]
        params['form'] = form
    else: #ただ開いた時
        params['form'] = HikaruForm()

    return render(request, 'user/hikaruSys.html', params)


def newBack(request):
    params = {'message': 'newです'}
    return render(request, 'user/new.html', params)

def hikaruSysBack(request):
    params = {'ans': '', 'form': None}
    if request.method == 'POST': # フォームで送信した時
        form = HikaruForm(request.POST)
        params['ans'] = request.POST['ans']
        params['ans'] = ['う','く']
        params['form'] = form
    else: #ただ開いた時
        params['form'] = HikaruForm()
    return render(request, 'user/hikaruSys.html', params)
