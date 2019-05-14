/*
    参数表
*/
-- 公共机构码表
create table if not exists ggjgm (
    jgm text primary key,
    -- 0 机构码
    mc text,
    -- 1 机构中文名称
    jc text,
    -- 3 机构简称  00、01 类型的机构存放分行的简称
    zfhh text,
    -- 7 大额支付行号
    jglx text,
    --15 机构类型  00-总行清算中心，01-总行营业部，10-分行清算中心，11-分行营业部，12-支行
    kbrq date,
    --16 开办日期
    hzjgm text --17 汇总机构码
);--内部账户开立模板
create table if not exists ggnbzhmb (
    jglx text,
    -- 机构类型，00-总行清算中心，01-总行营业部，10-分行清算中心，11-分行营业部，12-支行营业部
    whrq date,
    -- 维护日期
    kmh text,
    -- 科目号
    bzh text,
    -- 币种号  00-所有币种，B1-常用币种
    zhxx int,
    -- 账户序号
    hmgz int,
    -- 户名规则 0-按科目，1-指定名称
    hm text,
    -- 指定户名
    tzed real,
    -- 透支额度
    zhzt text,
    -- 账户状态 第1位：0-开户，1-销户；第二位：0-正常，1-借冻，2-贷冻，3-双冻；第三位：0-不可收付现，1-可收付现
    jxbz text,
    -- 计息标志 第1位：0-不计息，1-按月，2-按季，3-按年；第2位：0-计息不入账，1-入收息，2-入付息
    primary key (jglx, kmh, bzh, zhxx)
);
/*
create table 
if not EXISTS ggbzb 
-- 公共币种表
(
    bzh   text primary key , -- 币种号
    gbh     text,       -- 国标号
    bzmc    text,       -- 币种名称
    ywsx    text,       -- 英文缩写
    hltzcs  
)
*/