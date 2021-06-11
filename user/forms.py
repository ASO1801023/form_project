from django import forms

 
class UserForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    email = forms.EmailField(label='メール', max_length=100)
    ans = forms.CharField(label='答え', max_length=100)

class HikaruForm(forms.Form):
    ans = forms.CharField(label='答え', max_length=100)

    def clean_ans(self):
        ans = self.cleaned_data['ans']
        if(ans.find('<') != -1 or ans.find('>') != -1):
            raise forms.ValidationError("button1の文字が未入力")
        elif(ans.endswith("ん") or ans.endswith("ー")):
            raise forms.ValidationError("しりとりが出来ない文字で終わっているよ！")
        return ans
        

#一覧画面　新規作成
#class IdeaTreeForm(forms.ModelForm):
#    name = forms.CharField(label='名前', max_length=100)
#    overview = forms.CharField(label='概要', max_length=300)
#    complete_flag = forms.IntegerField()
#    idea_theme = forms.CharField(label='テーマ', max_length=300)
#    lastidea_id = forms.IntegerField()
#    user = forms.IntegerField()

#    class Meta:
#        model = IdeaTree
#        fields = ("name", ) #受け入れ
#        exclude = () #無視