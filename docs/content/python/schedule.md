---
title: Python job scheduling
weight: 511000
---

## Install

```
pip install schedule
```

## Usage

```python
import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
```

## References

- [Github](https://github.com/dbader/schedule)
- [stack overflow](https://stackoverflow.com/questions/34589347/run-python-script-every-10-seconds)
