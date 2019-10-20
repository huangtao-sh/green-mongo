create table if not exists txl(
    br text,
    -- 机构
    dept text,
    -- 部门
    name text,
    -- 姓名
    title text,
    -- 职务
    tel text,
    -- 电话
    fax text,
    -- 传真
    mobile text,
    -- 手机
    email text -- 电子邮件
);create index if not exists mobile_index on txl (mobile);create index if not exists email_index on txl(email);