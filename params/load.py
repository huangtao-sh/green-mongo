import zipfile
from orange import HOME, Path, limit
from trans import JyJiaoyi, JyShbs, JyCdjy, JyMenu, JyGangwei
from asyncio import run, wait
from glemon import P, FileImported
from .jgm import GgJgm
from .zh import AcTemplate
from orange.datautil import Data
from glemon import Document, dup_check
from glemon.bulk import BulkWrite
from .branch import Branch, Contacts
from .dengji import EduDengji
from .accounting import Accounting
from contextlib import suppress
from gmongo.params.teller import load_teller2

ROOT = HOME / 'OneDrive/工作/参数备份'

path = ROOT.find('运营参数*')

FileList = (
    (JyMenu, (ROOT / '交易菜单').find('menu*.xml')),
)
LoadFiles = (
    (Contacts, (ROOT / '通讯录').find('通讯录*.xls')),
    (Branch, (ROOT / '分行表').find('分行顺序表.xlsx')),
    (JyGangwei, (ROOT / '岗位与交易组').find('岗位及组*.xls')),
    (EduDengji, (ROOT / '额度登记配置').find('额度登记配置*.xls')),
    (Accounting, (ROOT / '科目说明').find('*.txt')),
)


def sjdr():
    for cls, filename in LoadFiles:
        if filename:
            try:
                print(f'开始处理 {cls.__name__}')
                result = cls.loadfile(filename)
                print(f'{cls.__name__} 处理成功，共导入数据 {result.inserted_count}条')
            except Exception as e:
                print(e)


async def load(Doc, path, *args):
    try:
        result = await Doc.sync_load_file(path, *args)
        if result:
            print(f'{path.name} 导入完成！')
            print(result)
    except Exception as e:
        print(e)


def main(dry=False):
    sjdr()          # 原数据导入模块
    coros = [load(*row) for row in FileList]  # 新的异步导入模块
    coros.append(load_param())
    run(wait(coros))


def read(z: zipfile.ZipFile, name: str, pipelines=None, encoding='GBK', errors='strict', sep=','):
    def _open(z, name):
        with z.open(name) as f:
            for line in f:
                row = line.decode(encoding=encoding, errors=errors).split(sep)
                yield [col.strip() for col in row]
    return Data(_open(z, name), pipelines)


def get(d, lst):
    return {x: d.pop(x) for x in lst if x in d}


async def loadfile(z: zipfile.ZipFile, doc: Document, name, dry: bool = False):
    options = doc.load_options or {}
    blk = BulkWrite(doc, data=read(
        z, name, **get(options, ['pipelines', 'encoding', 'errors', 'sep'])), **options)

    if dry:
        for obj in limit(blk, 100):
            print(obj)
    else:
        try:
            checker = dup_check(z.filename, doc.__name__) if options.pop(
                'dupcheck', True) else None
            if options.pop('drop', True):
                doc.objects.delete()
            result = await blk.sync_execute()
            if checker:
                checker.done()
            print(f'导入 {name.filename} 完成')
            print(result)
        except Exception as e:
            print(e)


ParamList = {
    'transactions_output': JyJiaoyi,
    'YUNGUAN_MONTH_STG_TELLER_SCANVOUCHER': JyShbs,
    'YUNGUAN_MONTH_STG_TELLER_TRANSCONTROLS': JyCdjy,
    'YUNGUAN_MONTH_STG_ZSRUN_GGJGM': GgJgm,
    'YUNGUAN_MONTH_STG_ZSRUN_GGNBZHMB': AcTemplate,
}


async def load_param():
    path = (HOME/'OneDrive/工作/参数备份').find('运营参数*.zip')
    with zipfile.ZipFile(path)as z:
        files = {}
        for fileinfo in z.filelist:
            if not (fileinfo.flag_bits & 0x0800):
                fileinfo.filename = fileinfo.filename.encode(
                    'cp437').decode('gbk')
                z.NameToInfo[fileinfo.filename] = fileinfo
            files[Path(fileinfo.filename).pname] = fileinfo
        load_teller2(path, z, files.get("users_output"))
        coros = [loadfile(z, doc, files.get(name))
                 for name, doc in ParamList.items()]
        await wait(coros)


def test(name):
    path = (HOME/'OneDrive/工作/参数备份').find('运营参数*.zip')
    doc = ParamList.get(name)
    if doc:
        with zipfile.ZipFile(path)as z:
            files = {}
            for fileinfo in z.filelist:
                if not (fileinfo.flag_bits & 0x0800):
                    fileinfo.filename = fileinfo.filename.encode(
                        'cp437').decode('gbk')
                    z.NameToInfo[fileinfo.filename] = fileinfo
                files[Path(fileinfo.filename).pname] = fileinfo
            if files.get(name):
                run(loadfile(z, doc, files.get(name), dry=True))


# test('stg_zsrun_ggnbzhmb')
