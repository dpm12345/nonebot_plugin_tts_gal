# 这里是关于自定义的用法指导(目前只支持VITS的.pth模型)

## 下载模型和与之对应的配置文件

对于该方面的内容，除了以往的两个模型外，支持添加其他的与之类似的模型

这里就以之前的两个模型为例进行解释

>以下是这两个模型的下载链接

| 模型                                                         | 配置文件                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [YuzuSoft_365_epochs.pth](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/EXTQrTj-UJpItH3BmgIUvhgBNZk88P1tT_7GPNr4yegNyw?e=5mcwgl) | [config.json](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/Ed7PXqaBdllAki0TPpeZorgBFdnxirbX_AYGUIiIcWAYNg?e=avxkWs) |
| [ATRI_vits_900E_G_38000.pth](https://pan.baidu.com/s/1_vhOx50OE5R4bE02ZMe9GA?pwd=9jo4) | 在前面的ATRI的下载链接里                                     |

下载好后，将model文件`.pth`放入`data/nonebot_plugin_tts_gal/model`文件目录中

将配置文件放入`data/nonebot_plugin_tts_gal/config`文件目录中

将相对应的模型文件和配置文件命名为同一个文件名（很重要，后面会说为什么)

如：下载好的柚子社多人模型，模型名初始为`365_epochs.pth`，配置文件名为`config.json`，这里可以将其分别命名为`YuzuSoft.pth`和`YuzuSoft.json`

## 修改机器人的配置文件

找到机器人的使用配置文件`.env.*`

在文件中添入以下内容

```
tts_gal = '{
    ("宁宁", "绫地宁宁"): ["YuzuSoft",0],
    ("因幡爱瑠", "爱瑠"): ["YuzuSoft",1],
    ("朝武芳乃", "芳乃"): ["YuzuSoft",2],
    ("常陸茉子", "茉子"): ["YuzuSoft",3],
    ("丛雨", "幼刀"): ["YuzuSoft",4],
    ("鞍馬小春", "鞍马小春", "小春"): ["YuzuSoft",5],
    ("在原七海", "七海"): ["YuzuSoft",6],
    ("ATRI", "atri", "亚托莉"): ["ATRI"],
}'
```

其中，`tts_gal`不能改,每一行的前半部分为触发的角色关键词

如第一行`("宁宁", "绫地宁宁"): ["YuzuSoft",0]`,"宁宁"，"绫地宁宁"即为让角色说时所触发的关键词。

紧跟在后面的`["YuzuSoft",0]`为模型名和角色语音对应的序号。这里的`YuzuSoft`与其角色使用的模型相对应，名字相同(均为`YuzuSoft`),`0`为角色对应的序号，是在多人模型中角色对应的序号id，如果添加的不是多人模型，那么可以如上面的`("ATRI", "atri", "亚托莉"): ["ATRI"]`，在名字后面不添加任何内容



在添加其他的VITS模型时，请注意模型分享者的模型类别，多人模型还是单人模型，并根据提供的信息以上面的格式在其基础上更改机器人配置项

**请一定要保持该格式，否则可能会出现错误**


## 再如富婆妹的模型
[model](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/ERNCwIXf51JGrkDODZ2Iy5oBpPKDPEvnd486ypQQyGmzZQ?e=1sSIED)
[config_file](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/EbYG4z3PmwhKibN59Sb8GTkBHr7gvbz6tWtsuwkmtqB8oA?e=cbxH86)

下载好后的文件分别为`604_epochs.pth`,`config.json`，如果将其命名为`fupomei`,

那么再根据下载来的模型配置文件可知,以下角色

```
['和泉妃愛', '常盤華乃', '錦あすみ', '鎌倉詩桜', '竜閑天梨', '和泉里', '新川広夢', '聖莉々子']
```

那么在`.env.*`中修改

```
tts_gal = '{
    ("宁宁", "绫地宁宁"): ["YuzuSoft",0],
    ("因幡爱瑠", "爱瑠"): ["YuzuSoft",1],
    ("朝武芳乃", "芳乃"): ["YuzuSoft",2],
    ("常陸茉子", "茉子"): ["YuzuSoft",3],
    ("丛雨", "幼刀"): ["YuzuSoft",4],
    ("鞍馬小春", "鞍马小春", "小春"): ["YuzuSoft",5],
    ("在原七海", "七海"): ["YuzuSoft",6],
    ("ATRI", "atri", "亚托莉"): ["ATRI"],
    ("和泉妃爱","妃爱"): ["fupomei",0],
    ("常盤華乃","常盘华乃","华乃"): ["fupomei",1],
    ("錦あすみ","锦亚澄"): ["fupomei",2],
    ("鎌倉詩桜","镰仓诗樱"): ["fupomei",3],
    ("竜閑天梨","龙闲天梨","天梨"): ["fupomei",4],
    ("和泉里"): ["fupomei",5],
    ("新川広夢","新川广梦"): ["fupomei",6],
    ("聖莉々子","圣莉莉子"): ["fupomei",7],
}'
```
重新启动机器人即可
