# If iOS returns an error similar to "Command PhaseScriptExecution failed with a nonzero exit code",

## on Terminal
``` 
flutter clean
flutter pub get
flutter pub upgrade
```

## on XCode, 
Show Project Navigator -> Project -> Info -> Configurations -> each target (and also each target with in the target) -> set configurations to None
[Screenshot](https://gitlab.com/asarangaram/snippets-screenshot/-/blob/main/PhaseScriptExecution_failed.png)

## again on Terminal, 
```
cd iOS
rm -rf Pods/ Podfile.lock
pod install
pod update 
```

