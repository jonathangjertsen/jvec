from jvec.framework import CountingSemaphore, Representable


def test_counting_semaphore():
    semaphore = CountingSemaphore()
    assert semaphore.value == 0
    assert not semaphore

    semaphore.dec()
    assert semaphore.value == 0
    assert not semaphore

    semaphore.inc()
    assert semaphore.value == 1
    assert semaphore

    semaphore.inc()
    assert semaphore.value == 2
    assert semaphore


def test_representable():
    params = { 'key1': 'value1', 'key2': 'value2' }
    rep = Representable(**params)
    rep.load_params(params, params.copy())

    rep_repr = repr(rep)
    rep_data = rep.data()
    rep_export = rep.export()

    assert rep_repr == "Representable(canvas, key1='value1', key2='value2')"
    assert rep_data == {
        'key1': 'value1',
        'key2': 'value2',
    }
    assert rep_export == {
        **rep_data,
        '__repr__': rep_repr,
    }

