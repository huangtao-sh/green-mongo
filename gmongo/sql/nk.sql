create table if not exists djr(
    gh  text    primary key, -- 工号
    djr text        -- 登记人
);
create table if not exists nkwg(
    ssjg    text,   -- 所属机构 
    dsrgh   text,   -- 当事人工号
    dsrxm   text,   -- 当事人姓名
    sstx    text,   -- 所属条线
    wtly    text,   -- 问题领域
    fssj    text,   -- 发生时间
    jjcd    text,   -- 紧急程度
    fxcd    text,   -- 风险程度
    sfqrwwt text,   -- 是否确认为问题
    lrjg    text,   -- 录入机构
    lrrgh   text,   -- 录入人工号
    lxrxm   text,   -- 录入人姓名
    sfkhjlr text,   -- 是否考核记录人
    jjcf    text,   -- 经济处罚
    kfz     int,    -- 扣分值
    zrrqr   text,   -- 登记事项责任人确认
    lrsj    text,   -- 录入时间
    shsj    text,   -- 审核时间
    shzt    text,   -- 审核状态
    djbh    text    primary key,    -- 登记编号
    lcbh    text,   -- OA流程号
    fxqk    text,   -- 发现情况
    clqk    text,   -- 处理情况
    jczt    text,   -- 检查主体
    zgzt    text,   -- 整改状态
    wfgd    text,   -- 违反规定
    zgjg    text,   -- 整改结果
    kfyjlb  text,   -- 扣分依据类别
    kfyjnr  text    -- 扣分依据内容
);