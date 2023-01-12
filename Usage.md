# 这里是关于自定义的用法指导(目前只支持VITS的.pth模型)

## 0.3.0版本的变动

在0.3.0版本中，增加了对中文模型的支持，为了兼容之前版本，正常使用翻译，在模型配置文件中需要加上`language`项,并且需要关注`text_cleaners`这一项内容，具体可以看[模型配置文件的要求](https://github.com/dpm12345/nonebot_plugin_tts_gal/blob/master/Usage.md#模型配置文件的要求)



## 功能解释

1. 生成语音功能。[name]说|发送[text]

   当`name`前有若干个空格时，同样也会触发

   `text`的长度至少为1

   当配置项`tts_gal_is_at`为`true`时，使用该功能需要@机器人

   当配置项`tts_gal_prefix`不为空时，使用该功能需要加上前缀，如`tts_gal_prefix = "tts"`，使用时`tts 宁宁说早上好。`

2. 翻译的调用

   1. 优先级：配置项的翻译项排列顺序决定了优先级，如`["baidu","tencent","youdao"]`，将会优先调用百度翻译，当翻译失败会自行调用腾讯翻译，失败后顺次往下

   2. 自动禁用翻译项：当翻译api返回余额不足、欠费等相关错误码时，会自动将该翻译项禁用，之后的翻译也不会调用，直到下个月第一天的00:05:00自动解禁

      (注:请自行注意使用api的使用量，及时处理)

   3. 手动禁用：可以使用`禁用 xxx`来禁用某一翻译项，禁用后，不会再调用该翻译项，月初也不会自动解禁，只能通过手动`启用翻译 xxx`来进行解禁

   4. 默认为调用`youdao`，且该翻译项不允许禁用

## 各类配置文件的配置

### 机器人配置文件要求

机器人配置文件为`.env.*`，其中`*`为`.env`中`ENVIRONMENT`配置项的值

这里至少需要配置`tts_gal`

<details>
<summary>tts_gal</summary> 

该配置项采用python的`字典`，其中`键`为`元组`，值为`列表`

`键`代表的角色语音的触发角色名,采用`元组`形式,如`("宁宁","绫地宁宁”)`，那么触发该角色语音名`name`为`宁宁`或者`绫地宁宁`

`值`代表该角色对应的模型相关信息,采用`列表`，元素个数至少为1，如`["YuzuSoft",0]`，`YuzuSoft`为该角色对应模型及配置名(即模型名为`YuzuSoft.pth`，配置名为`YuzuSoft.json`),`0`为多人模型所特有的，用以确认该角色序号，具体可以通过模型作者的提供信息获知(如果使用的为单人模型，那么可以不填或填`0`)

那么将以上内容结合，得到`("宁宁", "绫地宁宁"): ["YuzuSoft",0]`那么在配置文件中的形式为

```
tts_gal = '{
    ("宁宁", "绫地宁宁"): ["YuzuSoft",0],
}'
```

</details>

其他配置项按需要根据[README.md](https://github.com/dpm12345/nonebot_plugin_tts_gal/blob/master/README.md#%EF%B8%8F-配置)选填

### 模型配置文件的要求

模型配置文件至少需要保持下面格式

```
{
  "train": {
    ......
    "segment_size": 8192,
    ......
  },
  "data": {
    ......
    "text_cleaners":["japanese_cleaners"],
    "sampling_rate": 22050,
    "filter_length": 1024,
    "hop_length": 256,
    "add_blank": true,
    "n_speakers": 0,
    ......
  },
  "model": {
    "inter_channels": 192,
    "hidden_channels": 192,
    "filter_channels": 768,
    "n_heads": 2,
    "n_layers": 6,
    "kernel_size": 3,
    "p_dropout": 0.1,
    "resblock": "1",
    "resblock_kernel_sizes": [3,7,11],
    "resblock_dilation_sizes": [[1,3,5], [1,3,5], [1,3,5]],
    "upsample_rates": [8,8,2,2],
    "upsample_initial_channel": 512,
    "upsample_kernel_sizes": [16,16,4,4],
    "n_layers_q": 3,
    "use_spectral_norm": false
  },
  "language": "ja"
}

```

#### 关于data项里的text_cleaners

目前暂时只支持

+ japanese_cleaners
+ japanese_cleaners2
+ japanese_tokenization_cleaners
+ chinese_cleaners2

在导入配置文件时请注意该项的值，按需选择

#### 关于language

该配置项主要用于确认文本翻译目标，以下为各类语言对应的值

> 中文: zh-CHS
> 英语: en
> 日语: ja
> 韩语: ko
> 法语: fr
> 德语: de
> 俄语: ru
> 西班牙语: es
> 葡萄牙语: pt
> 意大利语: it
> 越南语: vi
> 印尼语: id
> 阿拉伯语: ar
> 荷兰语: nl
> 泰语: th

#### 关于symbols

这里推荐在json文件里自行添加，因为各自训练的symbols可能会有些许差异,具体symbols可以查看模型作者提供的信息。如果未设置symbols值，会根据`language`配置项选择默认的symbols

(目前默认只支持ja和zh-CHS,原因为zh-CHS的symbols通过json难以手动导入)

## 例子示例

对于该方面的内容，除了以往的两个模型外，支持添加其他的与之类似的模型

这里就以下面模型为例进行解释

### 模型下载

>以下是柚子社多人模型的下载链接

| 模型                                                         | 配置文件                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [YuzuSoft_365_epochs.pth](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/EXTQrTj-UJpItH3BmgIUvhgBNZk88P1tT_7GPNr4yegNyw?e=5mcwgl) | [config.json](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/Ed7PXqaBdllAki0TPpeZorgBFdnxirbX_AYGUIiIcWAYNg?e=avxkWs) |

### 配置文件修改

下载好后，将model文件`.pth`放入`data/nonebot_plugin_tts_gal/model`文件目录中

将配置文件放入`data/nonebot_plugin_tts_gal/config`文件目录中

将相对应的模型文件和配置文件命名为同一个文件名

如：下载好的柚子社多人模型，模型名初始为`365_epochs.pth`，配置文件名为`config.json`，这里可以将其分别命名为`YuzuSoft.pth`和`YuzuSoft.json`

#### 修改模型配置文件

打开`YuzuSoft.json`文件，由于该模型为日语模型，那么设置`"language": "ja"`,配置文件中的`text_cleaners`和`symbols`均满足上述要求，可以不改

#### 修改机器人的配置文件

找到机器人的使用配置文件`.env.*`

根据模型作者提供的信息，在文件中添入以下内容

```
tts_gal = '{
    ("宁宁", "绫地宁宁"): ["YuzuSoft",0],
    ("因幡爱瑠", "爱瑠"): ["YuzuSoft",1],
    ("朝武芳乃", "芳乃"): ["YuzuSoft",2],
    ("常陸茉子", "茉子"): ["YuzuSoft",3],
    ("丛雨", "幼刀"): ["YuzuSoft",4],
    ("鞍馬小春", "鞍马小春", "小春"): ["YuzuSoft",5],
    ("在原七海", "七海"): ["YuzuSoft",6],
}'
```

在添加其他的VITS模型时，请注意模型分享者的模型类别，多人模型还是单人模型，并根据提供的信息以上面的格式在其基础上更改机器人配置项

**请一定要保持该格式，否则可能会出现错误**
