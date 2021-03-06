import collections
import typing as t


# lol https://stackoverflow.com/posts/6027615/revisions
def flatten_dict_keys(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict_keys(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


def update_dict_sets(d1, d2):
    '''Given two dicts d1, d2 mapping keys to sets, extend the sets in d1 using
    the sets in d2. Keys present in d2 but missing in d1 are added to d1.

    d1 is mutated, d2 is not.

    >>> d1 = {'a': {1, 2}}
    >>> d2 = {'a': {1, 3}, 'b': {1}}
    >>> update_dict_sets(d1, d2)
    >>> d1
    {'a': {1, 2, 3}, 'b': {1}}
    >>> d2
    {'a': {1, 3}, 'b': {1}}
    '''
    for k, v in d2.items():
        if k in d1:
            d1[k].update(v)
        else:
            d1[k] = set(v)


def get_keys_as(d: dict, *keys: t.Union[t.Hashable, t.Tuple[t.Hashable]]) -> dict:
    '''Extract the keys from d and return a new dict with the keys optionally
    renamed.

    Example:
        >>> d = {'a': 1, 'b': 2}
        >>> get_keys_as(d, 'a', ('b', 'c'))
        {'a': 1, 'c': 2}

    :d dict to extract from
    :keys *args of either bare keys to extract or tuples of (old_key, new_key)
    '''
    acc = {}
    for _key in keys:
        if isinstance(_key, tuple):
            key, new_key = _key
            acc[new_key] = d[key]
        else:
            acc[_key] = d[_key]
    return acc
