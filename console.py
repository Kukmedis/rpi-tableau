from cfg import bus


@bus.on('counter:updated')
def display(name, counter):
    print(name, counter)