#! /usr/bin/env python

# Comment :
t = 1
if t:
    print "Here we are !!"


def fib(n):
    """Print a Fibonacci series up to n."""
    a, b = 1, 1
    while b < n:
        print b,
        a, b = b, a + b


fib(2000)
