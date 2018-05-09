from CodexMRS.base.network import Server


def test(message):
    print(message)


Server(test, "localhost").start_listening()
