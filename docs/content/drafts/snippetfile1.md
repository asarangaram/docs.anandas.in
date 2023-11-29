# Are you getting an error as shown in this [screenshot](https://gitlab.com/asarangaram/snippets-screenshot/-/blob/main/iProxyError.png)?

Delete /flutter/bin/cache/artifact directory. 

If it didn't work:
This is a permission issue, we may want to run the iProxy flutter/bin/cache/artifacts/usbmuxd/iproxy  and add into exception

[Source](https://stackoverflow.com/questions/71359062/iproxy-cannot-be-opened-because-the-developer-cannot-be-verified)