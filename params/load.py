import zipfile
from orange import HOME, Path, limit
from trans import JyJiaoyi, JyShbs, JyCdjy, JyMenu
from asyncio import run, wait
from glemon import P
from .jgm import GgJgm
from orange.datautil import Data
from glemon import Document, dup_check
from glemon.bulk import BulkWrite

ROOT = HOME / 'OneDrive/工作/参数备份'

path = ROOT.find('运营参数*')

FileList = (
    # (JyJiaoyi, path.find('transactions_output.*')),
    # (JyShbs, path.find('stg_teller_scanvoucher.*')),
    # (JyCdjy, path.find('stg_teller_transcontrols.*')),
    (JyMenu, (ROOT / '交易菜单').find('menu*.xml')),
    # (GgJgm, path.find('stg_zsrun_ggjgm.*')),
)


async def load(Doc, path, *args):
    try:
        result = await Doc.sync_load_file(path, *args)
        if result:
            print(f'{path.name} 导入完成！')
            print(result)
    except Exception as e:
        print(e)


def main(dry=False):
    coros = [load(*row) for row in FileList]
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
        for obj in limit(blk, 10):
            print(obj)
    else:
        try:
            # checker = dup_check(z.filename, doc.__name__) if options.pop(
            #    'dupcheck', True) else None
            checker = None
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
    'stg_teller_scanvoucher': JyShbs,
    'stg_teller_transcontrols': JyCdjy,
    'stg_zsrun_ggjgm': GgJgm,
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
            run(loadfile(z, doc, files.get(name), dry=True))

# test('stg_zsrun_ggjgm')
