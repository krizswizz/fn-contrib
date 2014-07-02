# Inspired by underscore.array.builders
import fn
from fn import _

existy = fn.F(_ != None)
isiterable = fn.func.partial(fn.func.flip(isinstance), fn.iters.Iterable)
isscalar = fn.F(fn.iters.not_) << isiterable

def cat(*args):
    '''Concatenates one or more iterables given as arguments.'''

    def p(arg):
        return (arg,) if isscalar(arg) else arg

    args_it = map(p, args)
    head = fn.iters.head(args_it)
    if not existy(head): return iter(())

    return fn.iters.chain(head, *args_it)

def cons(head, tail):
    '''Constructs an iterable by putting an element at its front.'''
    return cat((head,), tail)

def chunk(iterable, n, pad=None):
    '''Takes an iterable and partitions it some number of times into sub-arrays
    of size n. Allows an optional padding iterable to fill in the tail
    partition when n is not sufficient to build partitions of the same size.'''
    def p(it):
        part = tuple(fn.iters.take(n, it))

        if n == len(part): return cons(part, p(it))
        if not existy(pad): return ()

        return (tuple(fn.iters.take(n, cat(part,
                                           fn.iters.cycle(cat(pad))))),)

    return p(iter(iterable))

def chunk_all(iterable, n, step=None):
    '''Takes an iterable and partitions it some number of times into sub-arrays
    of size n. If the iterable given cannot fill the size needs of the final
    partition then a smaller partition is used for the last.'''
    step = step if existy(step) else n

    def p(it):
        head = tuple(fn.iters.take(n, it))
        if not len(head): return cat()
        return cons(head,
                    p(fn.iters.drop(step - n, it)) if len(head) == n
                    else ())

    return p(iter(iterable))

def mapcat(iterable, func):
    '''Maps a function over an iterable and concatenates all of the results.'''
    def p(arg):
        return (arg,) if isscalar(arg) else arg

    return cat(*map(p, map(func, iterable)))

def interpose(iterable, inter):
    '''Returns an iterator whith some item between each element of a given
    iterable'''
    if not isiterable(iterable): raise TypeError

    def p(it):
        it1, it2 = fn.iters.tee(it)
        head = fn.iters.head(it1)
        if not existy(head): return cat()
        try:
            next(fn.iters.tail(it2))
            return cons(head, cat((inter,), p(it1)))
        except StopIteration:
            return cons(head, ())

    return p(iterable)

def weave(*iterables):
    '''Weaves two or more iterables together.'''
    return filter(existy,
                  fn.iters.chain.from_iterable(
                      fn.iters.zip_longest(*iterables)))

def repeat(t, elem=None):
    '''Returns an iterable of a value repeated a certain number of times
    '''
    return fn.iters.repeat(elem, t) if existy(elem) else cat()

def cycle(t, iterable):
    '''Returns an iterable built from the contents of a given iterable
    repeated a certain number of times.
    '''
    return fn.iters.chain.from_iterable(fn.iters.repeat(tuple(iterable), t))

def split_at(iterable, index):
    '''Returns an iterable with two internal tuples built from
    taking an original iterable and splitting it at an index.
    '''
    it = iter(iterable)
    return (fn.iters.take(index, it), it)

def iterate_until(doit, checkit, seed):
    '''Call a function recursively until checkit predicate goes falsey.
    Expects a seed value to start.'''
    def p(arg):
        result = doit(arg)
        if checkit(result):
            return cat(result, p(result))
        return cat()

    return p(seed)

def take_skipping(iterable, n):
    '''Takes every nth item from an iterable, returning an iterator of the
    results.'''

    def p(it):
        val = fn.iters.nth(it, n - 1)
        if not existy(val): return cat()
        return cons(val, p(it))

    if n < 1: return cat()
    if n == 1: return iter(iterable)

    it = iter(iterable)
    return cons(fn.iters.nth(it, 0), p(it))

def reductions(iterable, func, init=None):
    '''Returns an  iterator of each intermediate stage of a call to a
    ``reduce``-like function.'''
    def p(acc, it):
        try:
            result = func(acc, next(it))
        except StopIteration:
            return cat()

        return cons(result, p(result, it))

    return p(init, iter(iterable))

def keep_indexed(iterable, pred):
    '''Runs its given function on the index of the elements rather than
    the elements themselves, keeping all of the truthy values in the end.
    '''
    return filter(None, fn.iters.starmap(pred, enumerate(iterable)))

def reverse_order(iterable):
    '''Accepts an iterable as an argument and returns an iterator whose
    elements are in the reverse order.
    '''
    return reversed(iterable)
