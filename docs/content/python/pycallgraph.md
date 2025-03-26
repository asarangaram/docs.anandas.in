A while ago I made [`pycallgraph`](https://pycallgraph.readthedocs.io/en/master/) which generates a visualisation from your Python code. **Edit:** I've updated the example to work with 3.3, the latest release as of this writing.

After a `pip install pycallgraph` and installing [GraphViz](http://www.graphviz.org/) you can run it from the command line:

```python
pycallgraph graphviz -- ./mypythonscript.py
```

Or, you can profile particular parts of your code:

```python
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

with PyCallGraph(output=GraphvizOutput()):
    code_to_profile()
```

Either of these will generate a `pycallgraph.png` file similar to the image below:

![enter image description here](https://i.sstatic.net/aiNEA.png)

https://stackoverflow.com/a/11822995