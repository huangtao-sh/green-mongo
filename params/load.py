from orange import HOME
from trans import JyJiaoyi, JyShbs, JyCdjy, JyMenu
from asyncio import run, wait
from glemon import P

ROOT = HOME / 'OneDrive/工作/参数备份'

path = ROOT.find('运营参数*')

FileList = (
    (JyJiaoyi, path.find('transactions_output.*')),
    (JyShbs, path.find('stg_teller_scanvoucher.*')),
    (JyCdjy, path.find('stg_teller_transcontrols.*')),
    (JyMenu, (ROOT / '交易菜单').find('menu*.xml')),
)


async def load(Doc, path, *args):
    result = await Doc.sync_load_file(path, *args)
    if result:
        print(f'{path.name} 导入完成！')
        print(result)


def main(dry=False):
    run(wait([load(*row) for row in FileList]))