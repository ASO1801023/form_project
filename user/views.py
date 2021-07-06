from django.shortcuts import render
from .forms import UserForm
from .forms import HikaruForm
from .forms import IdeaTreeForm
from django.db.models import Max

# hikaruSys sta
from janome.tokenizer import Tokenizer
import requests
from bs4 import BeautifulSoup
import codecs
import jaconv

from collections import Counter
import random
import pandas as pd
import csv
import pprint
import locale
from csv import reader
import codecs
# hikaruSys end

from user.models import Publisher
from user.models import IdeaTree
from user.models import Element

# 漢字をひらがな start
from pykakasi import kakasi
# 漢字をひらがな end

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'user/index.html')

#一覧画面処理
def list(request):
    #ログインしているuserを取得する処理
        
    ideatree_incomp = IdeaTree.objects.filter(complete_flag=0) #未完成ideaTreeを取得 (, user=1)
    ideatree_comp = IdeaTree.objects.filter(complete_flag=1) #未完成ideaTreeを取得

    ideatree_form = IdeaTreeForm()

    context = {
        'ideatree_incomp' : ideatree_incomp,
        'ideatree_comp' : ideatree_comp,
        'ideatree_form' : ideatree_form,
    }
    return render(request, 'user/list.html', context)

def list_2(request):
    params = {'c':''}
    newTheme = request.POST['newTheme']
    #一覧画面から
    if 'newButton' in request.POST:
        IdeaTree(name="新しいプロジェクト", overview="概要", complete_flag="0", idea_theme=newTheme, lastidea_id="0", user_id="1", passcode="999999").save()
        a = IdeaTree.objects.filter().count()
        b = IdeaTree.objects.filter()
        c = b[a-1].id
        Element(name="しりとり", path=1, color="1", ideatree_id=c).save()
        params['c'] = c
        return render(request, 'user/list_2.html', params)


def completed(request):
    # urlからidを取得 start
    now_urlid = 0
    if 'ideatreeid' in request.GET:
        now_urlid = request.GET['ideatreeid']
    # urlからidを取得 end

    params = {'ans': ''}

    ideatree_obj = getIdeaTree(now_urlid) #ideatree取得
    element_s = Element.objects.filter(ideatree_id=ideatree_obj['id']) # Elmentを全取得
    elem_lastnum = int(len(element_s)) # 葉っぱの数 == 最後の数字

    params['element_s'] = element_s #全ての葉っぱ

    params['ideatree_obj'] = ideatree_obj
    params['element_s'] = Element.objects.filter(ideatree_id=ideatree_obj['id'])
    return render(request, 'user/completed.html', params)


def hikaruSys(request): #メインページ処理

    # urlからidを取得 start
    now_urlid = 0
    if 'ideatreeid' in request.GET:
        now_urlid = request.GET['ideatreeid']
    # urlからidを取得 end

    params = {'ans': '', 'form': None}

    ideatree_obj = getIdeaTree(now_urlid) #ideatree取得
    element_s = Element.objects.filter(ideatree_id=ideatree_obj['id']) # Elmentを全取得
    elem_lastnum = int(len(element_s)) # 葉っぱの数 == 最後の数字


    if request.method == 'POST': # フォームで送信した時

        form = HikaruForm(request.POST) #フォームの型を形成(個数とバリデーション)

        if 'button1' in request.POST: #テキストボックスのを使う時
            firstInput = request.POST['ans']

        if 'button2' in request.POST: #候補ボタンを押した時
            firstInput = request.POST['button2']

        tegoshiWords = tegoshiSystem(firstInput)
        params['ruy1'] = tegoshiWords[0]
        params['ruy2'] = tegoshiWords[1]
        params['ruy3'] = tegoshiWords[2]
        params['sir1'] = tegoshiWords[3]
        params['sir2'] = tegoshiWords[4]
        params['sir3'] = tegoshiWords[5]

        params['form'] = form

        insertElement(firstInput,elem_lastnum,ideatree_obj['id']) #DB 登録
        
    else: #ただ開いた時

        params['element_s'] = element_s #全ての葉っぱ
        tegoshiWord_s = tegoshiSystem(params['element_s'][elem_lastnum-1].name) # 最後の言葉を手越システムにかける[path-1=配列番号]
        params['ruy1'] = tegoshiWord_s[0]
        params['ruy2'] = tegoshiWord_s[1]
        params['ruy3'] = tegoshiWord_s[2]
        params['sir1'] = tegoshiWord_s[3]
        params['sir2'] = tegoshiWord_s[4]
        params['sir3'] = tegoshiWord_s[5]

        params['form'] = HikaruForm()

    params['ideatree_obj'] = ideatree_obj
    params['element_s'] = Element.objects.filter(ideatree_id=ideatree_obj['id'])
    return render(request, 'user/hikaruPage.html', params)


def getIdeaTree(acc): # 指定したidのideatreeを取得
    retData = {'dummy': ''}
    ideatree_obj = IdeaTree.objects.filter(id=acc)
    retData['id'] = ideatree_obj[0].id
    retData['name'] = ideatree_obj[0].name
    retData['overview'] = ideatree_obj[0].overview
    retData['complete_flag'] = ideatree_obj[0].complete_flag
    retData['idea_theme'] = ideatree_obj[0].idea_theme
    retData['lastidea_id'] = ideatree_obj[0].lastidea_id
    return retData

def insertElement(acc,num,ideatree_id): # 言葉をElmentに登録
    Element(name=acc, path=num+1, color="2", ideatree_id=ideatree_id).save()
    return


def tegoshiSystem(acc):
    retData = [0] * 6
    ruyWords = ruySystem(acc)
    siriWords = siritoriSystem(acc)
    retData[0] = ruyWords[0]
    retData[1] = ruyWords[1]
    retData[2] = ruyWords[2]
    retData[3] = siriWords[0]
    retData[4] = siriWords[1]
    retData[5] = siriWords[2]
    return retData


def ruySystem(acc): #類義語システム(江崎作)
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
 

def siritoriSystem(acc): #しりとりシステム(かずなり作)
    retData = [0] * 3
    # しりとりサイド
    df = pd.read_csv('japanese.csv')

    # オブジェクトをインスタンス化
    kakasir = kakasi()
    # モードの設定：J(Kanji) to H(Hiragana)
    kakasir.setMode('J', 'H')
    # モードの設定：K(Katakana) to H(Hiragana)
    kakasir.setMode('K', 'H')
    # 変換して出力
    conv = kakasir.getConverter()
    secInput = conv.do(acc)  # => ひらがな化

    # 入力された文字がcsvになかった場合、文字を追加
    with open('Japanese.csv', encoding='utf-8') as f:
        csvList = csv.reader(f)
        flatList = [item for subList in csvList for item in subList]

        list = [acc]
        a = flatList.count(acc)

        if a == 0:
            with open('Japanese.csv', "a", encoding='utf-8') as wf:
                writer = csv.writer(wf)
                writer.writerow(list)
    del list

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


def willComplete(request):
    params = {'ans': '', 'form': None}
    # urlからidを取得 start
    now_urlid = 0
    if 'ideatreeid' in request.GET:
        now_urlid = request.GET['ideatreeid']
    # urlからidを取得 end

    ideatree_obj = getIdeaTree(now_urlid) #ideatree取得
    params['element_s'] = Element.objects.filter(ideatree_id=now_urlid) # Elmentを全取得

    params['ideatree_obj'] = ideatree_obj
    return render(request, 'user/willCompletePage.html', params)

def completeSys(request): 
    nowId = request.POST['nowId']
    newName = request.POST['newName'] # テキストボックスから入手
    newOverView = request.POST['newOverView'] # テキストボックスから入手

    ideatree_obj = IdeaTree.objects.filter(id=nowId)
    IdeaTree(id=ideatree_obj[0].id, name=newName, overview=newOverView, complete_flag='1', idea_theme=ideatree_obj[0].idea_theme, lastidea_id=ideatree_obj[0].lastidea_id, user_id=ideatree_obj[0].user_id, passcode=ideatree_obj[0].passcode).save()

    return render(request, 'user/completePage.html')


# 初期(使わない)

def new(request):
    params = {'message': 'newです'}
    return render(request, 'user/new.html', params)

def search(request):
    params = {'ans': '', 'form': None}
    if request.method == 'POST':
        #送信ボタンが押された時
        if 'set' in request.POST:
            TreeID = IdeaTree.objects.filter(passcode=request.POST['treeID'])
            ideatree_obj = getIdeaTree(TreeID[0].id) #ideatree取得
            element_s = Element.objects.filter(ideatree_id=ideatree_obj['id']) # Elmentを全取得
            elem_lastnum = int(len(element_s)) # 葉っぱの数 == 最後の数字

            params['form'] = HikaruForm()

        #randomボタンが押された時
        elif 'random' in request.POST:
            #aaaTreeID = IdeaTree.objects.filter(passcode__gte='0')
            #ideatreeを全て取得
            aaaTreeID = IdeaTree.objects.all()
            #ideatreeの数を数える
            TreeIDcount = IdeaTree.objects.all().count()
            num = random.randint(0,TreeIDcount)
            if num>=1:
                num=num-1

            #randomTreeID = random.shuffle(aaaTreeID)
            ideatree_obj = getIdeaTree(aaaTreeID[num].id)
            element_s = Element.objects.filter(ideatree_id=ideatree_obj['id']) # Elmentを全取得
            elem_lastnum = int(len(element_s)) # 葉っぱの数 == 最後の数字

            params['form'] = HikaruForm()
        
        elif 'random2' in request.POST:
            return render(request, 'user/random.html', params)



        params['element_s'] = Element.objects.filter(ideatree_id=ideatree_obj['id'])

    return render(request, 'user/search.html', params)

def random(request):
    #ideatreeを全て取得
    ideatree_obj = IdeaTree.objects.all()
    #ideatreeの数を数える
    TreeIDcount = IdeaTree.objects.all().count()
    num1 = random.randint(0,TreeIDcount)
    if num1>=1:
        num1=num1-1
    num2 = random.randint(0,TreeIDcount)
    if num2>=1:
        num2=num2-1
    num3 = random.randint(0,TreeIDcount)
    if num3>=1:
        num3=num3-1
    num4 = random.randint(0,TreeIDcount)
    if num4>=1:
        num4=num4-1

    #complete_flagが１のideatreeを取得
    params['comp_count'] = IdeaTree.objects.filter(complete_flag=1)
    cnt = len(params['comp_count'])
    if(cnt<4):
        str = ['ideatree1','ideatree2','ideatree3','ideatree4']
        for n in str:
            params[n] = IdeaTree.objects.all()

    else:
        params['ideatree1'] = getIdeaTree[num1]
        params['ideatree2'] = getIdeaTree[num2]
        params['ideatree3'] = getIdeaTree[num3]
        params['ideatree4'] = getIdeaTree[num4]

    return render(request, 'user/random.html', params)

