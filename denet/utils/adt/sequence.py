

class Sequencer:
    """
        Sequentially run a queue of functions on a given data

        TODO: sequencer should have an API for controlling outer flow from inner functions
    """
    def __init__(self):
        self.__base = dict()

    def enqueue(self, descriptor, func):
        self.__base[descriptor] = func

    def execute(self, data):
        res = data
        for descriptor in self.__base:
            res = self.__base[descriptor](res)
            print(f'PREPROCESSOR: {descriptor} -> {res}')

        return res


# m = Sequencer()
#
#
# def check(x):
#     if type(x) != str:
#         raise TypeError("Not valid type")
#     return x
#
#
# def process(string: str):
#     return string.upper()*4
#
#
# m.enqueue('Type Checker', check)
# m.enqueue('Process', process)
# m.execute("hello world")
# m.execute("50")
