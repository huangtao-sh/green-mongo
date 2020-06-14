/*
    营业主管问题一览表
*/

create table if not exists report(          -- 营业主管履职报告
    title text ,                             -- 标题
    period text,                            -- 期次
    name text,                              -- 报告人
    br text,                                -- 机构 
    date text,                              -- 报告日期
    cc text,                                -- 抄送
    attachment text,                        -- 附件
    yxqk text,                              -- 设备运行情况
    sbmc text,                              -- 异常设备名称
    ycnr text,                              -- 异常内容
    spyj text,                              -- 审批意见
    fhjj text,                              -- 分行解决
    zhjj text,                              -- 总行解决
    shryj text,                             -- 审核人意见
    fzryj text,                             -- 负责人意见
    content text,                           -- 内容，包括 类别、重要性、内容
    primary key(title,br)
);

drop table if exists bg;

create table if not exists bg(  -- 报告情况
    title text, -- 报告标题
    period  text,-- 报告期次
    name text,  -- 报告人
    br   text,  -- 机构
    date text,  -- 报告日期
    lx  text,    -- 报告类型 
    primary key(title,br)
);

create table
if not exists branch
-- 屏蔽机构清单，出现在本清单的机构，不需要报送
(
    br text unique,                         -- 机构号
    name text                               -- 机构名称
);

create table
if not exists lzwenti
(
    type text,                -- 0-分管行长，1-运营主管，2-营业主管 
    period text,              -- 运营主管：2018-1；营业主管： 2018-01  
    category text null,       -- 运营主管：分行序号，营业主管：问题分类 
    rpt_branch text,          -- 报告机构 
    rpt_name text,            -- 报告人
    content text,             -- 问题内容
    reply text null,          -- 答复意见
    reply_depart text null,   -- 答复部门
    reply_name text null,     -- 答复人
    state text null,          -- 状态跟踪
    importance bool null      -- 重要性
);
/*
    分管行长、运营主管报告
*/
create table
if not exists brreport
(
    period text,            -- 报告期 ，2018-1
    type text,              -- 类型：0-分管行长，1-运营主管
    branch text,            -- 分行
    name text,              -- 姓名
    date text,              -- 报告时间
    content text,           -- 报告内容
    primary key
(period,type,branch)
);
/*
    分行序列表
*/
create table
if not exists brorder
(
    brname  text primary key,       -- 分行名称
    brorder int,                     -- 序号
    state   bool                     -- 状态
);

create table
if not exists lzwt
(
    period      text,
    importance  text,
    category    text,
    branch      text,
    content     text,
    reporter    text,
    reply_dept  text,
    reply       text,
    status      text
);
create table if not exists yyzg(
	gyh		text primary key, -- 柜员号
	ygh		text,		-- 员工号
	xm		text,		-- 姓名
	js		text,		-- 角色
	lxdh	text,		-- 联系电话
	mobile	text,		-- 手机
	yx		text,		-- 邮箱
	bz		text,		-- 备注
	jg		text,		-- 机构号
	jgmc	text,		-- 机构名称
	whrq	text		-- 维护日期
);