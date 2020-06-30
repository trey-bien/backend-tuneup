#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Trey Dickerson"

from collections import Counter
import cProfile
import pstats
import functools
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        prof = cProfile.Profile()
        prof.enable()
        result = func(*args, **kwargs)
        prof.disable()
        stats = pstats.Stats(prof).strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats()
        return result
    return wrap


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False

@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


def timeit_helper(src):
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(src)
    result = t.repeat(repeat=4, number=3)
    average = min(result)
    print(f'Best timing of 4 repeats of 3 runs per repeat: {average} sec')
    return result
    
def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

timeit_helper(main)


if __name__ == '__main__':
    main()
