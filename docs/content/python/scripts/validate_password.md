---
title: Validate password
---

# Validate password

A valid password must contain at least one lowercase letter, one uppercase
letter, one digit and one special character, and be 7-20 characters long.
Each rule is expressed as a separate lookahead:

```python
reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{7,20}$"
```

Snippet to validate:

```python
import re


def validate_pw(password):
    return re.search(re.compile(reg), password) is not None
```

See the [runnable version with tests](../notebooks/validate_passwords.ipynb).
