class MyClass:
    number = 0
    name = "noname"

def Main():
    me = MyClass()
    me.number = 1337
    me.name = "Draps"

    friend = MyClass()
    friend.number = 3
    friend.name = "Steve"

    empty = MyClass()

    print("Name: " + me.name + ", favorite number: " + str(me.number))
    print("Name: " + friend.name + ", favorite number: " + str(friend.number))
    print("Name: " + empty.name + ", favorite number: " + str(empty.number))

if __name__ == '__main__':
    Main()
