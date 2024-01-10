async def say_hello():
    print("Hello!")


async def say_goodbye():
    print("Goodbye!")


async def meet_and_greet():
    await say_hello()
    print("How have you been?")
    print("I've been good, you?")
    print("Me too.")
    await say_goodbye()


def run(coro):
    try:
        coro.send(None)
    except StopIteration:
        ...


if __name__ == "__main__":
    run(meet_and_greet())
