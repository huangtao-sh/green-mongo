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


create table if not exists xxbm(
	bm		text 	primary key,  -- 编码
	name	text,	-- 名称
	km		text	-- 科目
);
