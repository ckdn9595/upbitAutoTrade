import asyncio
from csv import DictReader

import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler.eventloop import AsyncIOScheduler

from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


def csv_to_generator(csv_file_path):
   
    for row in DictReader(open(csv_file_path, 'r')):
        point = Point('financial-analysis') \
            .tag('type', 'vix-daily') \
            .field('open', float(row['VIX Open'])) \
            .field('high', float(row['VIX High'])) \
            .field('low', float(row['VIX Low'])) \
            .field('close', float(row['VIX Close'])) \
            .time(row['Date'])
        yield point


async def main():
    bucket="crypto"
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "upbit-trade"
    url = "http://3.36.115.87:8086"
    async with InfluxDBClientAsync(url=url, token=token, org=org) as client:
        write_api = client.write_api()

        async def async_write(batch):
            await write_api.write(bucket=bucket, record=batch)
            return batch

        batches = rx \
            .from_iterable(csv_to_generator('vix-daily.csv')) \
            .pipe(ops.buffer_with_count(500)) \
            .pipe(ops.map(lambda batch: rx.from_future(asyncio.ensure_future(async_write(batch)))), ops.merge_all())

        done = asyncio.Future()
        
        batches.subscribe(on_next=lambda batch: print(f'Written batch... {len(batch)}'),
                          on_error=lambda ex: print(f'Unexpected error: {ex}'),
                          on_completed=lambda: done.set_result(0),
                          scheduler=AsyncIOScheduler(asyncio.get_event_loop()))
        
        await done


if __name__ == "__main__":
    asyncio.run(main())