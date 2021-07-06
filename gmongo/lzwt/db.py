# 项目：   履职报告问题
# 模块：   数据库
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-06-21 20:15

from orange.utils.sqlite import db_config, executescript
db_config('~/.data/lzwt.db')
executescript('''
create table if not exists lzwtzt(
    rq      text,   -- 报告日期，营业主管格式：2021-01，分管行长及运营管理部负责人格式：2021-1
    lx      text,   -- 类型：1-分管行长及运营管理部负责人，2-运营主管
    zt      text,   -- 状态：0-待处理，1-待审核，2-待发布,9-结束
    primary key(rq,lx)
);
create table if not exists lzwt(
    bh      text  primary key,   -- 问题编号
    rq      text,   -- 报告日期
    lx      text,   -- 类型：0-分管行长，1-运营管理部负责人，2-营业主管
    jg      text,   -- 机构
    bgr     text,   -- 报告人
    wtfl    text,   -- 问题分类
    wtms    text,   -- 问题
    dfbm    text,   -- 答复部门
    dfr     text,   -- 答复人
    dfyj    text,   -- 答复意见
    ldyj    text,   -- 领导意见
    zt      text,   -- 处理状态：待提交需求，已提交需求，待投产，待解决，待研究
    ywxq    text,   -- 业务需求
    jyw     text    -- 校验位：从问题分类到状态的校验位
)
''')
