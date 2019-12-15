from glemon import Document, P
from pymongo import InsertOne
from orange import datetime, split
import asyncio


class Test(Document):
    _projects = '_id', 'name', 'age'

    @classmethod
    def load1(cls, data):
        for row in data:
            cls(row).save()
        cls.drop()

    @classmethod
    def load2(cls, data):
        for r in split(data, 10000):
            cls._collection.bulk_write([InsertOne(row) for row in r])
        print(cls.objects.count())
        cls.drop()

    @classmethod
    async def load3(cls, data):
        coros = [
            cls._acollection.bulk_write([InsertOne(row) for row in d])
            for d in split(data, 10000)
        ]
        await asyncio.wait(coros)
        print(cls.objects.count())
        cls.drop()

    @classmethod
    async def load4(cls, data):
        MAX_CUS = 5

        async def prod(q, data):
            for d in split(data, 10000):
                await q.put(d)
            for i in range(MAX_CUS):
                await q.put(None)
            await q.join()

        async def burk(q):
            while True:
                d = await q.get()
                if d is None:
                    q.task_done()
                    break
                else:
                    await cls._acollection.bulk_write(
                        [InsertOne(row) for row in d])
                    q.task_done()

        q = asyncio.Queue(maxsize=10)
        coros = [burk(q) for i in range(MAX_CUS)]
        await asyncio.wait([*coros, prod(q, data)])
        print(cls.objects.count())
        cls.drop()


def create_data(count=1000000):
    for i in range(count):
        yield dict(zip(Test._projects, (i, f'name-{i}', f'age-{i}')))


'''
s1 = datetime.now()
print(s1)
Test.load1(create_data())
t1 = datetime.now() - s1
print('load1', t1)

s1 = datetime.now()
Test.load2(create_data())
t2 = datetime.now() - s1
print('load2', ":", t2)

s1 = datetime.now()
asyncio.run(Test.load4(create_data()))
t2 = datetime.now() - s1
print('load4', ":", t2)
exit()

s1 = datetime.now()
asyncio.run(Test.load3(create_data()))
t2 = datetime.now() - s1
print('load3', ":", t2)
'''

