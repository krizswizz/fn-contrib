# tests from documentcloud.github.io/underscore-contrib/#array.builders
from nose import tools
from fncontrib import builder
import fn
from fn import _

def test_cat():
    dut = fn.F(tuple) << builder.cat

    tools.eq_(dut(), (), 'should return an empty tuple when given no args')
    tools.eq_(dut(()), (), 'should concatenate one empty tuple')
    tools.eq_(dut((1, 2, 3)), (1, 2, 3),
                  'should concatenate one homogenious tuple')
    tools.eq_(dut((1, '2', (3,), {'n': 4})),
              (1, '2', (3,), {'n': 4}),
           'should concatenate one homogenious tuple')
    tools.eq_(dut((1, 2, 3), (4, 5, 6)), tuple(range(1, 7)),
        'should concatenate two tuples')
    tools.eq_(dut(*map(tuple, fn.iters.grouper(3, range(1, 10)))),
            tuple(range(1, 10)),
              'should concatenate three tuples')
    # heterogenious types
    tools.eq_(dut((1,), 2), (1, 2), 'should concatenate mixed types')
    tools.eq_(dut((1,), 2, 3), (1, 2, 3), 'should concatenate mixed types')
    tools.eq_(dut(1, 2, 3), (1, 2, 3), 'should concatenate mixed type')

def test_cons():
    dut = fn.F(tuple) << builder.cons

    tools.eq_(dut(0, ()), (0,), 'should insert the first arg into iterable'
              'given as second arg')
    tools.eq_(dut(1, (2,)), (1, 2), 'should insert the first arg into iterable '
              'given as second arg')
    tools.eq_(dut((0,), (1, 2, 3)), ((0,), 1, 2, 3),
              'should insert the first arg into iterable given as second arg')
    tools.eq_(dut(1, 2), (1, 2),
            'should create a pair if the second is not iterable')

def test_chunk():
    dut = fn.F(tuple) << builder.chunk

    tools.eq_(dut(range(4), 2), ((0, 1), (2, 3)),
              'should chunk into the size given')
    tools.eq_(dut(range(5), 2), ((0, 1), (2, 3)),
              'should chunk into the size given, extras are dropped')
    tools.eq_(dut(range(7), 3, (7, 8)), ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
             'should allow one to specify a padding iterable')
    tools.eq_(dut(range(5), 3, 9), ((0, 1, 2), (3, 4, 9)),
              'should allow one to to specify a padding value')

def test_chunk_all():
    dut = fn.F(tuple) << builder.chunk_all

    tools.eq_(dut(range(4), 2), ((0, 1), (2, 3)),
              'should chunk into the size given')
    tools.eq_(dut(range(10), 4), ((0, 1, 2, 3), (4, 5, 6, 7),(8, 9)),
              'should chunk into the size given, with a small end')
    tools.eq_(dut(range(10), 2, 4), ((0, 1), (4, 5), (8, 9)),
              'should chunk into the size given, with skips')
    tools.eq_(dut(range(10), 3, 4), ((0, 1, 2), (4, 5, 6), (8, 9)),
              'should chunk into the size given, with skips and a small end')

def test_mapcat():
    dut = fn.F(tuple) << builder.mapcat
    cons = builder.cons

    tools.eq_(dut(range(1, 5), fn.func.partial(fn.func.flip(cons), ',')),
              (1,',', 2, ',', 3, ',', 4, ','),
              'should return an iterable with all intermediate iterables ' \
              'concatenated')

def test_interpose():
    dut = fn.F(tuple) << builder.interpose

    tools.eq_(dut(range(1, 4), 0), (1, 0, 2, 0, 3), 'should put the 2nd arg ' \
              'between the elements of the iterable given')
    tools.eq_(dut((1, 2), 0), (1, 0, 2), 'should put the 2nd arg between ' \
              'the elements of the iterable given')
    tools.eq_(dut((1,), 0), (1,), 'should return an iterable given if ' \
              'nothing to interpose')
    tools.eq_(dut((), 0), (), 'should return an empty iterable given an ' \
              'empty tuple')

def test_weave():
    dut = fn.F(tuple) << builder.weave

    # zero
    tools.eq_(dut(()), (), 'should weave zero iterables')
    # one
    tools.eq_(dut(()), (), 'should weave one iterable')
    tools.eq_(dut((1, (2,))), (1, (2,)), 'should weave one iterable')
    # two
    tools.eq_(dut(range(1, 4), (1, 2)), (1, 1, 2, 2, 3),
              'should weave two iterables')
    tools.eq_(dut(*fn.iters.tee(range(1, 4))), (1, 1, 2, 2, 3, 3,),
              'should weave two iterables')
    tools.eq_(dut(('a', 'b', 'c'), range(1, 4)), ('a', 1, 'b', 2, 'c', 3),
              'should weave two  iterables')
    tools.eq_(dut(range(1, 4), (1, (2,))), (1, 1, 2, (2,), 3),
              'should weave two iterables')
    # > 2
    tools.eq_(dut(range(1, 4), (1, 2), ('a', 'b', 'c')),
              (1, 1, 'a', 2, 2, 'b', 3, 'c'),
              'should weave more than two iterables')
    tools.eq_(dut(range(1, 4), (1, 2), ('a', 'b', 'c'), (1, (2,))),
              (1, 1, 'a', 1, 2, 2, 'b', (2,), 3, 'c'),
              'should weave more than two iterables')

def test_repeat():
    dut = fn.F(tuple) << builder.repeat

    tools.eq_(dut(3, 1), (1, 1 , 1), 'should build an iterator  of size n ' \
              'wthi the specified element in each slot')
    tools.eq_(dut(0), (), 'should return an empty iterable if given zero ' \
              'and no repeat arg')
    tools.eq_(dut(0, 9999), (), 'should return an empty iterable if ' \
              'given zero and some repeat arg')

def test_cylce():
    dut = fn.F(tuple) << builder.cycle

    tools.eq_(dut(3, range(1, 4)), (1, 2, 3, 1, 2, 3, 1, 2, 3),
              'should return an iterable with the specified content ' \
              'repeated n times')
    tools.eq_(dut(0, range(1, 4)), (), 'should return an empty iterable if ' \
              'told to repeat zero times')
    tools.eq_(dut(-1000, range(1, 4)), (), 'should return an empty iterable ' \
              'if told to repeat negative times')

def test_split_at():
    dut = fn.F(tuple) << fn.F(map, tuple) << builder.split_at

    tools.eq_(dut(range(1, 6), 2), ((1, 2), (3, 4, 5)),
              'should bifurcate an iterable at a given index')
    tools.eq_(dut(range(1, 6), 0), ((), tuple(range(1, 6))),
              'should bifurcate an iterable at a given index')
    tools.eq_(dut(range(1, 6), 5), (tuple(range(1, 6)), ()))
    tools.eq_(dut((), 5), ((), ()),
              'should bifurcate an iterable at a given index')

def test_iterate_until():
    dut = fn.F(tuple) << builder.iterate_until
    dec = fn.F(_ - 1)
    ispositive = fn.F(_ > 0)

    tools.eq_(dut(dec, ispositive, 6), tuple(range(5, 0, -1)),
              'should build an iterable, decrementing ')

def test_take_skipping():
    dut = fn.F(tuple) << builder.take_skipping

    tools.eq_(dut(range(5), 0), (), 'should take nothing if told to skip ' \
              'by zero')
    tools.eq_(dut(range(5), -1), (), 'should take nothing if told to skip ' \
              'negative')
    tools.eq_(dut(range(5), 1), tuple(range(5)), 'should take every element ' \
              'in an iterable')
    tools.eq_(dut(range(10), 2), tuple(range(0, 10, 2)), 'should take every ' \
              '2nd element in an iterable')

def test_reductions():
    dut = fn.F(tuple) << builder.reductions

    result = dut(range(1, 6), fn.F(_ + _), 0)
    tools.eq_(result, (1, 3, 6, 10, 15), 'should retain each itermediate ' \
              'step in a reduce')

def test_keep_indexed():
    dut = fn.F(tuple) << builder.keep_indexed

    oddy = lambda index, val: val if (val % 2) else None
    posy = lambda index, val: val if val > 0 else None

    a = tuple(range(6))
    tools.eq_(dut(a, oddy), (1, 3, 5), 'keeps elements whose index passes ' \
              'a truthy test')
    b = (-9, 0, 29, -7, 45, 3, -8)
    tools.eq_(dut(b, posy), (29, 45, 3), 'keeps elements whose index passes ' \
              'a truthy test')
