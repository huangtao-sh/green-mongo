/*
    假期表参数
    */

CREATE TABLE IF NOT EXISTS jqb(
    year  text primary key, -- 年份
    anpai   text, -- 安排
    ab      text  -- 1月1日的AB户标志
);

create table if not exists mailconf(
    user    text, -- 用户名
    passwd  text, -- 密码
    addr    text   -- 服务器地址
)