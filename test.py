from orange.utils.data import filterer, converter
from orange import Path, R
from orange.xlsx import Header


def cstr(width: int = 0) -> 'function':
    def _(val: int) -> str:
        return f'%0{width}d' % int(val)

    return _


@filterer
def row_filter(row):
    return isinstance(row[1], (int, float)) or R / r'\d{4}' == row[1]


conv = {
    0: str.strip,
    1: cstr(4),
    4: cstr(2),
    5: cstr(1),
    6: cstr(1),
    8: cstr(1),
    10: cstr(2)
}
for i in range(12, 21):
    conv[i] = cstr(1)

path = Path(
    r"C:/Users/huangtao/OneDrive/工作/当前工作/20190701新增交易码参数/交易码表20190701.xlsx")
data = path.sheets("新增", row_filter, converter(conv))

PrdHeaders = [
    Header('交易名称'),
    Header('现有系统交易码'),
    Header('交易所属交易组（编码）'),
    Header('交易所属交易组（中文名称）'),
    Header('交易所属优先级（两位数字）'),
    Header('网点交易授权级别:1－主办授权,2－主管授权'),
    Header('中心交易授权级别：1－主办授权，2－主管授权'),
    Header('必须网点授权？TRUE, FALSE'),
    Header('中心授权机构：0-总中心、1-分中心'),
    Header('必须中心授权？TRUE, FALSE'),
    Header('技能级别要求（两位数字）'),
    Header('CashIn：现金收\nCashOut：现金付\nTransIn：转账收、TransOut：转账付（现转账收与转账付相同）\n'
           '自助现金收SelfCashIn\n自助现金付SelfCashOut\n自助转账SelfTransIn/SelfTransOut'),
    Header('是否需要外包：1－不需要，2－需要'),
    Header('是否需要大额提示（大额核查，电话确认）：0－不需要，1－需要'),
    Header('是否需要扫描电子底卡 0-不扫描，1-扫描'),
    Header('是否需要收手续费 0-不需要，1-需要'),
    Header('是否需要后台监测：0－不需要，1－需要'),
    Header('事中监督扫描方式：0-不扫描，1-实时扫描，2-补扫\n0-不监督\n1-实时监督\n2-非实时监督'),
    Header('补扫的限时时间(分钟)'),
    Header('是否需要审查（用于调用审查规则的服务）：0－不需要，1－需要'),
    Header('是否允许抹账：0-不允许，1-允许'),
    Header('是否允许超额授权：TRUE－允许，FALSE－不允许'),
    Header('辅助交易组（需与主交易组不一致，以“|”分隔，例：TG001P|TG002P）可为空'),
    Header('是否需要事后补扫TRUE - 需要, FALSE - 不需要'),
    Header('磁道校验信息TRUE - 需要, FALSE - 不需要'),
]

for r in data:
    print(*r)
