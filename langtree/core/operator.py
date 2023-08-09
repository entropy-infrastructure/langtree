import backoff


def default_call(*args, **kwargs):
    return kwargs


def default_parse(output):
    return output


def freeze(function, **top_kwargs):
    def frozen(*args, **kwargs):
        return function(*args, **{**top_kwargs, **kwargs})

    return frozen


def chainable(func):
    def wrapper(**kws):
        return freeze(func, **kws)

    return wrapper


class Operator(object):

    def __init__(self, call=default_call, parse=default_parse):
        self.call = call
        self.parse = parse

    # @backoff.on_exception(backoff.expo(2, 2), Exception, max_tries=5)
    def __call__(self, *args, **kwargs):
        res = self.call(*args, **kwargs)

        if self.parse is not None:
            res = self.parse(res)

        return res

    def freeze_call(self, **kwargs):
        self.call = freeze(self.call, **kwargs)

    def freeze_parse(self, **kwargs):
        self.parse = freeze(self.parse, **kwargs)