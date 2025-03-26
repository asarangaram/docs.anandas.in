
**Python includes a profiler called [`cProfile`](https://docs.python.org/3/library/profile.html#module-cProfile).** It not only gives the total running time, but also times each function separately, and tells you how many times each function was called, making it easy to determine where you should make optimizations.

You can call it from within your code, or from the interpreter, like this:

```python
import cProfile
cProfile.run('foo()')
```

Even more usefully, you can invoke cProfile when running a script:

```python
python -m cProfile myscript.py
```

Or when running a module:

```python
python -m cProfile -m mymodule
```

To make it even easier, I made a little batch file called 'profile.bat':

```python
python -m cProfile %1
```

So all I have to do is run:

```python
profile euler048.py
```

And I get this:

```
1007 function calls in 0.061 CPU seconds

Ordered by: standard name
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    0.000    0.000    0.061    0.061 <string>:1(<module>)
 1000    0.051    0.000    0.051    0.000 euler048.py:2(<lambda>)
    1    0.005    0.005    0.061    0.061 euler048.py:2(<module>)
    1    0.000    0.000    0.061    0.061 {execfile}
    1    0.002    0.002    0.053    0.053 {map}
    1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler objects}
    1    0.000    0.000    0.000    0.000 {range}
    1    0.003    0.003    0.003    0.003 {sum}
```

For more information, check out this tutorial from PyCon 2013 titled [**_Python Profiling_**](https://web.archive.org/web/20170318204046/http://lanyrd.com/2013/pycon/scdywg/)  
[Also via YouTube](https://www.youtube.com/watch?v=QJwVYlDzAXs).

https://stackoverflow.com/a/582337

Comments:
https://docs.python.org/2/library/profile.html

Also it is useful to sort the results, that can be done by -s switch, example: '-s time'. You can use cumulative/name/time/file sorting options

## threads
It's worth pointing out that using the profiler only works (by default) on the main thread, and you won't get any information from other threads if you use them. This can be a bit of a gotcha as it is completely unmentioned in the [profiler documentation](http://docs.python.org/library/profile.html).

If you also want to profile threads, you'll want to look at the [`threading.setprofile()`function](http://docs.python.org/library/threading.html#threading.setprofile "threading.setprofile() function") in the docs.

You could also create your own `threading.Thread` subclass to do it:

```python
class ProfiledThread(threading.Thread):
    # Overrides threading.Thread.run()
    def run(self):
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(threading.Thread.run, self)
        finally:
            profiler.dump_stats('myprofile-%d.profile' % (self.ident,))
```

and use that `ProfiledThread` class instead of the standard one. It might give you more flexibility, but I'm not sure it's worth it, especially if you are using third-party code which wouldn't use your class.

https://stackoverflow.com/a/1922945
