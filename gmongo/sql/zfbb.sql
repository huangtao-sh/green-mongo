
create table if not exists PaymentData(  -- 支付数据表
    subno text,                          -- 期次
    at text,                             -- 类型
    ac text,                             -- 代码
    "in" text,                           -- 指标代码
    dn text,                             -- 纬度代码
    vv real,                             -- 值1
    vv2 real,                            -- 值2
    primary key(subno,at,ac,"in",dn)
);

create table if not exists parameter(
    "id" int primary key,   -- 序号
    "in" text,              -- 指标代码
    dn   text,              -- 纬度代码
    name text,              -- 指标名称
    rule int                -- 0-期末值，1-合计值
)