# -*- coding: utf-8 -*-

import json
import os
import re
import requests

def push(key,title,content):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token": key,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)

def login(womail_url):
    try:
        url = womail_url
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
        }
        res = requests.get(url=url, headers=headers, allow_redirects=False)
        set_cookie = res.headers["Set-Cookie"]
        cookies = re.findall("YZKF_SESSION.*?;", set_cookie)[0]
        if "YZKF_SESSION" in cookies:
            return cookies
        else:
            print("沃邮箱获取 cookies 失败")
            return None
    except Exception as e:
        print("沃邮箱错误:", e)
        return None

def dotask(cookies):
    msg = ""
    headers = {
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
        "Cookie": cookies,
    }
    try:
        url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
        res = requests.post(url=url, headers=headers)
        result = res.json()
        wxname = result.get("result").get("wxName")
        usermobile = result.get("result").get("userMobile")
        userdata = f"帐号信息: {wxname} - {usermobile[:3]}****{usermobile[-4:]}\n"
        msg += userdata
    except Exception as e:
        print("沃邮箱获取用户信息失败", e)
        msg += "沃邮箱获取用户信息失败\n"
    try:
        url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
        res = requests.post(url=url, headers=headers).json()
        result = res.get("result")
        if result == -2:
            msg += "每日签到: 已签到\n"
        elif result is None:
            msg += f"每日签到: 签到失败\n"
        else:
            msg += f"每日签到: 签到成功~已签到{result}天！\n"
    except Exception as e:
        print("沃邮箱签到错误", e)
        msg += "沃邮箱签到错误\n"
    try:
        url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
        data_params = {
            "每日首次登录手机邮箱": {"taskName": "loginmail"},
            "每日答题赢奖": {"taskName": "answer"},
            "礼遇金秋赢话费": {"taskName": "clubactivity"},
            "奥运每日答题": {"taskName": "clubactivity"},
            "下载沃邮箱app": {"taskName": "download"},
            "和WOWO熊一起寻宝": {"taskName": "treasure"},
            "去用户俱乐部逛一逛": {"taskName": "club"},
            "邀请好友关注沃邮箱": {"taskName": "club"},
        }
        for key, data in data_params.items():
            try:
                res = requests.post(url=url, data=data, headers=headers).json()
                result = res.get("result")
                if result == 1:
                    msg += f"{key}: 做任务成功\n"
                elif result == -1:
                    msg += f"{key}: 任务已做过\n"
                elif result == -2:
                    msg += f"{key}: 请检查登录状态\n"
                else:
                    msg += f"{key}: 未知错误\n"
            except Exception as e:
                print(f"沃邮箱执行任务【{key}】错误", e)
                msg += f"沃邮箱执行任务【{key}】错误"

    except Exception as e:
        print("沃邮箱执行任务错误", e)
        msg += "沃邮箱执行任务错误错误"
    return msg

def dotask2(womail_url):
    msg = ""
    userdata = re.findall("mobile.*", womail_url)[0]
    url = "https://club.mail.wo.cn/clubwebservice/?" + userdata
    headers = {
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
    }
    try:
        res = requests.get(url=url, headers=headers, allow_redirects=False)
        set_cookie = res.headers["Set-Cookie"]
        cookies = re.findall("SESSION.*?;", set_cookie)[0]
        if "SESSION" in cookies:
            headers = {
                "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
                "Cookie": cookies,
                "Referer": "https://club.mail.wo.cn/clubwebservice/club-user/user-info/mine-task",
            }
            # 获取用户信息
            try:
                url = "https://club.mail.wo.cn/clubwebservice/club-user/user-info/get-user-score-info/"
                res = requests.get(url=url, headers=headers)
                result = res.json()
                integraltotal = result.get("integralTotal")
                usermobile = result.get("userPhoneNum")
                userdata = f"帐号信息: {usermobile[:3]}****{usermobile[-4:]}\n当前积分:{integraltotal}\n"
                msg += userdata
                response = requests.get('https://club.mail.wo.cn/clubwebservice/growth/queryIntegralTask',
                                        headers=headers)
                integral_task_data = response.json()['data']
                integral_task_data.append({
                            "resourceName": "每日签到（积分）",
                            "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create",
                        })

                print(integral_task_data)
                lenth = len(integral_task_data)
                # msg+="--------积分任务--------\n"
                # 执行积分任务
                skip_task = ['俱乐部签到','沃邮箱网页版登录']
                for i in range(lenth):
                    resource_name = integral_task_data[i]["resourceName"]
                    try:
                        if resource_name in skip_task:
                            continue
                        if "每日签到" in resource_name:
                            url = integral_task_data[i]["url"]
                            res = requests.get(url=url, headers=headers).json()
                            result = res.get("description")
                            if "success" in result:
                                continuous_day = res["data"]["continuousDay"]
                                msg += f"{resource_name}: 签到成功~已连续签到{str(continuous_day)}天！\n"
                            else:
                                msg += f"{resource_name}: {result}\n"
                        else:
                            resource_flag = integral_task_data[i]["resourceFlag"]
                            resource_flag = resource_flag.replace("+", "%2B")
                            url = f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={usermobile}&resourceType={resource_flag}"
                            res = requests.get(url=url, headers=headers).json()
                            result = res.get("description")
                            msg += f"{resource_name}: {result}\n"
                    except Exception as e:
                        print(f"沃邮箱俱乐部执行任务【{resource_name}】错误", e)
                        msg += f"沃邮箱俱乐部执行任务【{resource_name}】错误"
            except Exception as e:
                print("沃邮箱俱乐部获取用户信息失败", e)
                msg += "沃邮箱俱乐部获取用户信息失败\n"
        else:
            msg += "沃邮箱俱乐部获取SESSION失败\n"
    except Exception as e:
        print("沃邮箱俱乐部获取cookies失败", e)
        msg += "沃邮箱俱乐部获取cookies失败\n"
    return msg

def main(url):
    try:
        cookies = login(url)
        if cookies:
            msg = dotask(cookies)
            msg += f"\n沃邮箱俱乐部\n{dotask2(url)}"
        else:
            msg = "登录失败"
    except Exception as e:
        print(e)
        msg = "登录失败"
    return msg


if __name__ == '__main__':
    env_demo = '''
    {
        "account": [{
            "push_token": "123456798",
            "womail_url": "http://baidu.com"
        }, {
            "push_token": "87654321",
            "womail_url": "http://google.com"
        }]
    }
    '''
    data = json.loads(os.getenv('data'))['account']
    for user in data:
        message = main(user['womail_url'])
        print(message)
        push(user['push_token'],'联通沃邮箱 - 签到', message)