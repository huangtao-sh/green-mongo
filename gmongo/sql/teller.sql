create table if not exists teller(
    id          text    PRIMARY key,   -- 柜员号
    name        text,   -- 姓名
    telephone   text,   -- 电话
    grade       text,   -- 柜员级别
    [group]     text,   -- 柜组
    branch      text,   -- 机构号
    userid      text,   -- 员工号
    post        text,   -- 岗位
    zxjyz       text,   -- 执行交易组
    zzxe        text,   -- 转账限额
    xjxe        text,   -- 现金限额
    rzlx        text,   -- 认证类型
    zt          text,   -- 状态
    pbjy        text,   -- 屏蔽交易
    gwxz        text,   -- 岗位性质
    qyrq        text,   -- 启用日期
    zzrq        text,   -- 终止日期
    jybz        text,   -- 交易币种
    fqjyz       text,   -- 发起交易组
    zjlx        text,   -- 证件类型
    zjhm        text,   -- 证件号码
    sfyy        text    -- 是否运营人员
);

create table if not exists eddj(
	code	text	primary key,	-- 等级代码
	name	text,	--	等级名称
	ed		text,	--	额度
	memo	text	-- 备注
)