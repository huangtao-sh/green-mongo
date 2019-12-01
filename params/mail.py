# 项目：   参数管理平台
# 模块：   邮箱配置
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-12-01 16:46

from glemon import Shadow
from orange.mail import MailClient, mail_config, Mail
from orange import arg

conf = Shadow.read('mail') or {}
if conf:
    mail_config(**conf)


@arg('-s', '--host', nargs='?', help='邮箱服务器')
@arg('-u', '--user', nargs='?', help='登录账号')
@arg('-p', '--passwd', nargs='?', help='密码')
def config_mail(**conf):
    try:
        MailClient(**conf)
        Shadow.write('mail', conf)
        mail_config(**conf)
        print('配置邮箱服务器成功')
    except:
        print('登录服务器失败')
