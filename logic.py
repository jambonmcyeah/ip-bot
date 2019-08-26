import miniupnpc
import asyncio

class IpGetter(object):
    def __init__(self, delay: int=200, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = miniupnpc.UPnP()
        self.client.discoverdelay = delay

        asyncio.ensure_future(self.connect())

    async def connect(self):
        try:
            if self.client.discover() > 0:
                self.client.selectigd()
            else:
                raise TimeoutError("No Router Found")
        except Exception as e:
            raise TimeoutError(e.args)

    async def get_external_ip(self, attempts: int=3, attempt: int=0) -> str:
        try:
            return self.client.externalipaddress()
        except Exception:
            await self.connect()
            if attempt < attempts:
                return await self.get_external_ip(attempts, attempt+1)
            else:
                raise TimeoutError("Failed to get external ip: Out of attempts")

    async def get_local_ip(self) -> str:
        return self.client.lanaddr