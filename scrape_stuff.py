import httpx


async def get_google():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://google.com')
        with open('google.html', 'wb') as writer:
            writer.write(r.content)


async def get_bing():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://bing.com')
        with open('bing.html', 'wb') as writer:
            writer.write(r.content)
