from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
 
User = get_user_model()
 

class HikaruForm(forms.Form):
    ans = forms.CharField(label='単語', max_length=100)

#    def clean_ans(self):
#        ans = self.cleaned_data['ans']
#        if(ans.find('<') != -1 or ans.find('>') != -1):
#            raise forms.ValidationError("button1の文字が未入力")
#        elif(ans.endswith("ん") or ans.endswith("ー")):
#            raise forms.ValidationError("しりとりが出来ない文字で終わっているよ！")
#        return ans

#class atsushiForm(forms.Form):

        

#一覧画面　新規作成
class IdeaTreeForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    overview = forms.CharField(label='概要', max_length=300)
    complete_flag = forms.IntegerField()
    idea_theme = forms.CharField(label='テーマ', max_length=300)
    lastidea_id = forms.IntegerField()
    user = forms.IntegerField()

    #class Meta:
    #    model = IdeaTree
    #    fields = ("name", ) #受け入れ
    #    exclude = () #無視
    #    exclude = () #無視


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'