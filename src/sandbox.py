

class Something:
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return f'{self.val}'
    def __repr__(self):
        return str(self)



def run():
    things = [Something(x) for x in range(10)]
    print(things)

    for i in range(len(things)):
        thing = things[i]
        thing.val += 1

    print(things)


if __name__=='__main__':
    run()