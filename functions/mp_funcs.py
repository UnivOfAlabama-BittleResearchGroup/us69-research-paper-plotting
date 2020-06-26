import multiprocessing
import pandas as pd
import numpy as np

CPU_COUNT = multiprocessing.cpu_count()


def _apply_df(args):
    df, func, num, kwargs = args
    return num, df.apply(func, **kwargs)


def apply_by_multiprocessing(df, func, **kwargs):
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ns.df = df
    pool = multiprocessing.Pool(processes=CPU_COUNT)
    result = pool.map(_apply_df, [(d, func, i, kwargs) for i, d in enumerate(np.array_split(ns.df, CPU_COUNT))])
    pool.close()
    mgr.shutdown()
    result = sorted(result, key=lambda x: x[0])
    return pd.concat([i[1] for i in result])


def _general_func(args):
    func, indexes, num, df, kwargs = args
    return num, func(indexes, df,**kwargs)


def shared_df_mp_func(iterable, func, shared_df, **kwargs):
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ns.df = shared_df
    pool = multiprocessing.Pool(processes=len(iterable))
    result = pool.map(_general_func, [(func, ind, i, ns.df, kwargs) for i, ind in enumerate(iterable=iterable)])
    pool.close()
    mgr.shutdown()
    result = sorted(result, key=lambda x: x[0])
    return result

