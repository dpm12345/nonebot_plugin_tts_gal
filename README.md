
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot_plugin_tts_gal

基于nonebot和vits的部分gal角色的语音合成插件

</div>



# 前言

本人python比较菜，因此可能有些地方写的比较屎，还望轻喷

# 安装

pip安装

```
pip install nonebot_plugin_tts_gal
```

nb-cli安装

```
nb plugin install nonebot-plugin-tts-gal
```



## 资源文件

下载`data`文件夹，并放入在bot的运行目录下

下载model文件

[YuzuSoft_365_epochs.pth](https://sjtueducn-my.sharepoint.com/:u:/g/personal/cjang_cjengh_sjtu_edu_cn/EXTQrTj-UJpItH3BmgIUvhgBNZk88P1tT_7GPNr4yegNyw?e=5mcwgl)

将文件重命名为`YuzuSoft_365_epochs.pth`

[ATRI_vits_900E_G_38000.pth](https://pan.baidu.com/s/1_vhOx50OE5R4bE02ZMe9GA?pwd=9jo4)

找到pth文件


最后将这两个pth文件放入到`data/nonebot_plugin_tts_gal/model/`下

## 相关依赖

ffmpeg的安装

#### Windows

在ffmpeg官网下载[ffmpeg下载](https://github.com/BtbN/FFmpeg-Builds/releases),选择对应的版本，下载后解压，并将位于`bin`目录添加到环境变量中

其他具体细节可自行搜索

#### Linux

Ubuntu下

```
apt-get install ffmpeg
```

或者下载源码安装(具体可搜索相关教程)

# 配置项

请在使用的配置文件(.env.*)加入

```
auto_delete_voice = True
```

用于是否自动删除生成的语音文件，如不想删除，可改为

```
auto_delete_voice = False
```



# 使用

群聊和私聊仅有细微差别，其中下面语句中，`name`为合成语音的角色，`text`为转语音的文本内容(会自动转为日文，故也可以输入中文)

## 群聊

`@机器人 [name]说[text]`

## 私聊

`[name]说[text]`

例如：宁宁说おはようございます.

目前`name`有

- 宁宁|绫地宁宁
- 因幡爱瑠|爱瑠
- 朝武芳乃|芳乃
- 常陸茉子|茉子
- 丛雨|幼刀
- 鞍馬小春|鞍马小春|小春
- 在原七海|七海
- ATRI|atri|亚托莉



# 今后

添加更多的模型



# 感谢

+ 部分代码参考自[nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet)

+ **[CjangCjengh](https://github.com/CjangCjengh/)**：g2p转换，适用于日语调形标注的符号文件及分享的[柚子社多人模型](https://github.com/CjangCjengh/TTSModels)
+ **[luoyily](https://github.com/luoyily)**：分享的[ATRI模型](https://pan.baidu.com/s/1_vhOx50OE5R4bE02ZMe9GA?pwd=9jo4)
