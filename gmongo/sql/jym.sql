/*
生产交易码表数表
*/
--drop table if exists jym;

CREATE TABLE IF NOT EXISTS jym(
    jym     text primary key,   --交易码
    jymc    text,   --交易名称
    jyz     text,   --交易组
    yxj     text,   --优先级
    wdsqjb  text,   --网点授权级别
    zssqjb  text,   --中心授权级别
    wdsq    text,   --网点授权
    zssqjg  text,   --中心授权机构
    zssq    text,   --中心授权
    jnjb    text,   --技能级别
    xzbz    text,   --现转标志
    wb      text,   --外包
    dets    text,   --大额提示
    dzdk    text,   --电子底卡
    sxf     text,   --手续费
    htjc    text,   --后台监测
    szjd    text,   --事中监督
    bssx    text,   --补扫时限
    sc      text,   --审查
    mz      text,   --抹账
    cesq    text,   --超额授权
    fjjyz   text,   --辅加交易组
    shbs    text default "TRUE",   --事后补扫
    cdjy    text default "FALSE"   --磁道校验
);

/* 交易菜单表 */
CREATE TABLE IF NOT EXISTS JYCD(
    jym     text  primary key,  --交易码
    jymc    text,       --交易名称
    yjcd    text,       --一级菜单
    ejcd    text        --二级菜单
);

-- 交易组表 
create table if not exists jyz(
    jyz     text    primary key, --交易组
    name    text                 --交易组名
);
-- 岗位表
create table if not exists jygw(
    id      int    primary key, -- 岗位代码
    code    text,               -- 岗位代码
    name    text                -- 岗位名称
);

-- 岗位交易组对照表
create table if not exists jyzgw(
    gw  text,         -- 岗位代码
    jyz text        -- 交易组
);


CREATE TABLE IF NOT EXISTS jycs(
    jym     text,   --交易码
    jymc    text,   --交易名称
    jyz     text,   --交易组
    yxj     text,   --优先级
    wdsqjb  text,   --网点授权级别
    zssqjb  text,   --中心授权级别
    wdsq    text,   --网点授权
    zssqjg  text,   --中心授权机构
    zssq    text,   --中心授权
    jnjb    text,   --技能级别
    xzbz    text,   --现转标志
    wb      text,   --外包
    dets    text,   --大额提示
    dzdk    text,   --电子底卡
    sxf     text,   --手续费
    htjc    text,   --后台监测
    szjd    text,   --事中监督
    bssx    text,   --补扫时限
    sc      text,   --审查
    mz      text,   --抹账
    cesq    text,   --超额授权
    fjjyz   text,   --辅加交易组
    shbs    text,   --事后补扫
    cdjy    text,   --磁道校验
    yjcd    text,   --一级菜单
    ejcd    text,   --二级菜单
    operation integer, --操作码 0-新增，1-修改，2-删除
    bz      text,   --备注
    zt      integer default 0,   --状态 0-提出，1-待投产，2-已投产，9-作废
    create_time      text,-- 创建时间
    validate_time    text,-- 投产时间
    primary key(create_time,jym)
);