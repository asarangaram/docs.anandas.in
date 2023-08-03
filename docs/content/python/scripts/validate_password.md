---
title: Validate password
---

Create a RegExp that represents valid password, like below.
```python
reg =   "^(?=.*\[a-z\])(?=.*\[A-Z\])(?=.*\\d)(?=.*\[@$!%*#?&\])\[A-Za-z\\d@$!#%*?&\]{6,20}$"
```

Snippet to validate
```python
def validate_pw(password)
    pat =   re.compile(reg)
    mat =   re.search(pat, passwd)
    if mat:
        return True
    else:
        return False
```
