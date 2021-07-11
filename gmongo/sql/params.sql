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

create table if not exists branch(
    jgm     text  primary key,  --机构码
    mc      text,
    brorder text
);

create table if not exists bzb(
    bz      text primary key,-- 币种号
    gbh     text, -- 国标号
    bzmc    text, -- 币种名称
    ywsx    text, -- 英文缩写
    hltzcs  text, -- 汇率调整参数
    hltzrq  text,   --汇率调整日期
    ws      real,   -- 尾数
    qybz    text,   -- 启用标志 0: 未用，1:启用，2:止用 
    qyrq    text,   -- 启用日期
    zyrq    text,   --止用日期
    dgqygz  text    --对公启用标志
/*
第一位: 结算
第二位: 同城
第三位: 联行
第4--8: 待定
0: 未用
1: 启用
2: 止用*/
);