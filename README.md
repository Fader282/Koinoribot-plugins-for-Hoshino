# KoinoriBot Plugins
![Python Version](https://img.shields.io/badge/python-3.8+-blue)
[![试用群](https://img.shields.io/badge/试用/一群-冰祈杂谈总铺-brightgreen)](https://jq.qq.com/?_wv=1027&k=o3WzKAfn)
[![试用群](https://img.shields.io/badge/试用/二群-冰祈杂谈分铺-brightgreen)](https://jq.qq.com/?_wv=1027&k=fdFbP60u)


基于HoshinoBot的冰祈插件集合 [![Hoshinobot Version](https://img.shields.io/badge/hoshino-2.1.0-blue)](https://github.com/Ice-Cirno/HoshinoBot) 


## 功能介绍

冰祈是一个多功能娱乐型群聊机器人，功能具体请移步 [使用指南](https://www.lanxy.ink/?p=476)

<details>
  <summary>仓库内功能一览</summary>

- **每日签到**：`icelogin`
- **更换称呼**：`call_me_please`
- **碧蓝档案**：查询学生资料，抽卡模拟器 `ba_wiki`
- **Arcaea查分** `Arcaea`
- **冰祈与鱼**：钓鱼与漂流瓶二合一 `fishing`
- **人脸卡通化**：`cartoon`
- **图片美学评分**：`DetectDisgust`
- **随机美图**：`sinaimg`
- 其他小型功能，具体可查看各自文件夹里的 `__init__.py` 文件

</details>

<details>
  <summary>其他hoshinobot插件功能</summary>

源于hoshinobot丰富的插件生态，冰祈也有相当一部分非原创功能来自 [HoshinoBot插件仓库](https://github.com/pcrbot/HoshinoBot-plugins-index)，具体可以自行检索。
</details>


## 使用方法

> - 下载本仓库，将koinoribot文件夹解压至 `hoshino/modules` 里。
> 
> 
> - 安装 `requirements.txt` 内的所有依赖。
> 
> 
> - 在 `hoshino/config/__bot__.py` 中的 `MODULES_ON` 里新增一行 `"koinoribot",`。

<details>
 <summary> 注意事项 </summary> 

 - 如果在安装依赖的过程中出现错误，请务必及时解决，通常都可在百度上找到解决方案。
 
 
 - 关于部分插件需要用到的静态图片资源文件与字体文件，恕不在此公开。如有需要可以移步[![插件试用群](https://img.shields.io/badge/插件试用-冰祈杂谈分铺-brightgreen)](https://jq.qq.com/?_wv=1027&k=fdFbP60u)。
 
 
 - 部分功能需要申请api，请将相应的api填进 `koinoribot/config.py` 里以正常使用插件。
 
 
 - 部分插件在下载图片时需要走代理，可以在 `koinoribot/config.py` 的 `proxies` 栏内进行配置。推荐使用 [clash](https://github.com/Fndroid/clash_for_windows_pkg)
</details>



<details>
 <summary> 关于如何安装hoshino </summary> 

- 仓库传送门 [Hoshinobot](https://github.com/Ice-Cirno/HoshinoBot) (作者： [Ice-cirno](https://github.com/Ice-Cirno))

</details>


## 个人部署环境参考
 - 服务器：Windows Server 2019
 - Python版本：3.8.0
 - 代理：clash for windows
 - Visual Studio 2019

