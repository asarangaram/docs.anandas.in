---
title: Implement Locking Mechanism to ensure single instance of an application
---
Imagine this scenario: you have a Python script that relies on resources that cannot be shared and require strict serialization. Running the script in parallel could potentially lead to data corruption. To prevent such issues, you need to implement a locking mechanism that ensures the script runs only once at any given time.

The simplest and effective solution is to use a file-based locking mechanism provided by the `singleton class` in the `tendo` library. This class creates a lock file with a filename based on the full path to the script file (over-ridable). The lock file prevents multiple instances of the script from running simultaneously, avoiding conflicts and data corruption. Moreover, the singleton class allows specific functions to have their own singleton instances, which can be achieved by providing an argument called flavor_id.

You can find the source code of this singleton class on [GitHub](https://github.com/pycontribs/tendo/blob/main/src/tendo/singleton.py).

