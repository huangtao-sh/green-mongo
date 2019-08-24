/*
交易码表
*/

CREATE TABLE IF NOT EXISTS jymb(
    jymc    text,   --交易名称
    jym     text primary key,   --交易码
    jyz     text,   --交易组
    jyzm    text,   --交易组名
    yxj     text,   --优先级
    wdsqjb  text,   --网点授权级别
    zssqjb  text,   --中心授权级别
    wdsq    text,   --网点授权
    zssq    text,   --中心授权
    zssqjg  text,   --中心授权机构
    jnjb    text,   --技能级别
    xzbz    text,   --现转标志
    wb      text,   --外包
    dets    text,   --大额提示
    dzdk    text,   --电子底卡
    szjd    text,   --事中监督
    bssx    text,   --补扫时限
    mz      text,   --抹账
    cesq    text,   --超额授权
    fzjyz   text,   --辅助交易组
    shbs    text,   --事后补扫
    cdjy    text    --磁道校验
);

CREATE TABLE IF NOT EXISTS JYCD(
    jym     text  primary key,  --交易码
    jymc    text,       --交易名称
    yjcd    text,       --一级菜单
    ejcd    text        --二级菜单
)