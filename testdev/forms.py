#coding:utf8
from django import forms
from django.forms import ModelForm
from django.forms import widgets  # 插件
from django.forms import fields  # 字段
from testdev.models import TestCase

###ContactForm(initial={'subject': 'Hi there!'})
'''
ContactForm(initial={'subject': 'Hi there!'})
f.fields['name'].label = "Username"
nick_name = CharField(required=False)
在子类中，可以通过设置名字为None 来删除从父类中继承的字段。例如：

>>> from django import forms

>>> class ParentForm(forms.Form):
...     name = forms.CharField()
...     age = forms.IntegerField()

>>> class ChildForm(ParentForm):
...     name = None

>>> ChildForm().fields.keys()
... ['age']
IntegerField¶

class IntegerField(**kwargs)¶
默认的Widget：当Field.localize 是False 时为NumberInput，否则为TextInput。
空值：None
规范化为：一个Python 整数或长整数。
验证给定值是一个整数。允许前导和尾随空格，如Python的int()函数。
错误信息的键：required, invalid, max_value, min_value
max_value和min_value错误消息可能包含%(limit_value)s，将替换为适当的限制。

采用两个可选参数进行验证：

max_value¶
min_value¶
它们控制字段中允许的值的范围。
'''
class AaForm(forms.Form):
    name = forms.CharField(30)
    passwrd = forms.CharField(30)
    openid = forms.CharField(30)
    roleid = forms.CharField(30)
    areaid =forms.CharField(10)


class GailvForm(forms.Form):
    pid = forms.CharField(30)
    uin = forms.CharField(30)
    sum = forms.CharField(30)
    areaid = forms.CharField(30)
    roleid=forms.CharField(30)
    url=forms.CharField(30)


class AcForm(forms.Form):
    openid = forms.CharField(30)
    roleid = forms.CharField(30)
    areaid = forms.CharField(10)


class AddTestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ['taskdesc', 'procallcount', 'amsid', 'metaruleid', 'production']


class GetTestCaseForm(forms.Form):
    production = forms.CharField(
        initial=3,  # 初始值为3
        widget=widgets.Select(choices=((1,'xxsy'), (2,'tlbb'),(3,'all')))  # 插件表现形式为下拉框
        #choices=((1, 'xxsy'), (2, 'tlbb'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
        #initial=1,  # 默认选中第二个option
        #widget=widgets.RadioSelect  # 插件表现形式为单选按钮
    )


class StressTestingForm(forms.Form):
    file = forms.FileField(label='上传用户号码包')
    uri = forms.URLField(label='*uri',
                         widget=forms.TextInput(
                             attrs={'placeholder': '示例：https://cgidev.datamore.qq.com/datamore/dnfcityfriend_external/profile'})
                         )
    method = forms.CharField(label='*选择请求方式',
                             initial=1,  # 初始值为1
                             widget=widgets.Select(choices=((1, 'get'), (2, 'post')))
                             )
    parms = forms.CharField(label='设置请求参数',
                            widget=forms.TextInput(
                                attrs={'placeholder': '示例：{"zoneid":"0","matchid":"8","index":"9"}'}),
                            required=False)
    headers = forms.CharField(label='设置header',
                              widget=forms.TextInput(
                                  attrs={'placeholder': '示例：{"cookie": "uin=o0783184998;skey=@FOPCE2Pap"}'}),
                              required=False)
    pos = forms.CharField(label='*用户信息所在位置',
                             initial=1,  # 初始值为1
                             widget=widgets.Select(choices=((1, 'headers'), (2, 'parms')))
                             )
    zhanghao = forms.CharField(label='*用户信息字段',
                               widget=forms.TextInput(
                                   attrs={'placeholder': '多个字段用,隔开，示例：uin,roleid,skey;注：字段顺序与用户包的列排序一致'})
                               )
    nub = forms.IntegerField(label='*最高并发数',
                             max_value=500,
                             min_value=10,
                             widget=forms.TextInput(attrs=
                                                    {'placeholder': '填写大于等于10，小于等于500的整数'})
                             )


class UploadFileForm(forms.Form):
    file = forms.FileField(label='上传用户号码包')
    uri = forms.URLField(label='*uri',
                         widget=forms.TextInput(
                             attrs={'placeholder': '示例：https://cgidev.datamore.qq.com/datamore/dnfcityfriend_external/profile'})
                         )
    method = forms.CharField(label='*选择请求方式',
                             initial=1,  # 初始值为1
                             widget=widgets.Select(choices=((1, 'get'), (2, 'post')))
                             )
    parms = forms.CharField(label='设置请求参数',
                            widget=forms.TextInput(
                                attrs={'placeholder': '示例：{"zoneid":"0","matchid":"8","index":"9"}'}),
                            required=False)
    headers = forms.CharField(label='设置header',
                              widget=forms.TextInput(
                                  attrs={'placeholder': '示例：{"cookie": "uin=o0783184998;skey=@FOPCE2Pap"}'}),
                              required=False)
    tofileds = forms.CharField(label='*目标字段',
                               widget=forms.TextInput(
                                   attrs={'placeholder': '多个字段用,隔开，示例：Data.sgp,Data.dgp,Data.tgp'}),
                               )

    pos = forms.CharField(label='*用户信息所在位置',
                             initial=1,  # 初始值为1
                             widget=widgets.Select(choices=((1, 'headers'), (2, 'parms')))
                             )
    zhanghao = forms.CharField(label='*用户信息字段',
                               widget=forms.TextInput(
                                   attrs={'placeholder': '多个字段用,隔开，示例：uin,roleid,skey;注：字段顺序与用户包的列排序一致'})
                               )
    floattoint = forms.IntegerField(label='转换倍数',
                                    widget=forms.TextInput(
                                        attrs={'placeholder': '3.54转354，此处填写100'}),
                                    required=False
                                    )
    nub = forms.IntegerField(label='*最高并发数',
                             max_value=500,
                             min_value=10,
                             widget=forms.TextInput(attrs=
                                                    {'placeholder': '填写大于等于10，小于等于500的整数'})
                             )