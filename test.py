import asyncio

async def foo(a):
    if a:
        print(a)
    else:
        print("Nothing")



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    a = 1
    loop.run_until_complete(foo(a))
    loop.run_until_complete(foo(a))