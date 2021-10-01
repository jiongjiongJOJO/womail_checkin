# 联通沃邮箱签到脚本
## 使用方法
自行通过抓包获得如下格式的GET链接：
```
https://nyan.mail.wo.cn/cn/sign/index/index?mobile=ABCDEFG&userName=&openId=HIJKLMNOPQRSTUVWXYZ
```
设置环境变量，其中key为`data`，value为如下格式的内容：
```
{
	"account": [{
		"push_token": "123456798",
		"womail_url": "http://baidu.com"
	}, {
		"push_token": "87654321",
		"womail_url": "http://google.com"
	}]
}
```
注意：准确填写json格式的数据内容，代码没做校验，报错就自己检测json是不是有问题。

## 参考文献
代码参考了 [Sitoi/dailycheckin](https://sitoi.github.io/dailycheckin) 提供的文件，本人只是做了结构上的修改和部分bug的修复。


## 免责声明
本项目为个人学习测试使用，禁止其他用途，非必要不fork，可以给个小星星(star)。

任何单位或个人认为通过本产品提供的软件可能涉嫌侵犯其合法权益，应该及时向作者书面反馈，并提供身份证明、权属证明及详细侵权情况证明，作者在收到上述法律文件后，将会尽快移除被控侵权软件。

如若侵犯了您的权益，请及时通过邮箱（41473909@qq.com）联系作者，作者会第一时间关闭仓库。