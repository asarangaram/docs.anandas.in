
### Dart Platform Channels on Linux 

There are many reasons, why method channel is required in Dart. I am not going to discuss, what is method channel, why do we need or when do we need. Instead, this article is just a quick guide to create a method channel and use it. (How part of the problem).

we make a very simple application that modifies the default counter application, and then increase the complexity with some explanation. Hope this helps to understand Method Channel.

Let us start with the default counter application. Create one using `flutter create counter_app`. In the default application generated with `**sdk 3.0.6**`, the counter is incremented by the function `_incrementCounter().` We shall only modify this function so that the counter is part of the platform code, and this function, just fetches the counter value using the method channel. 

Change the function `_incrementCounter()` as below. 

![Screen shot with git diff — to show required changes](https://cdn-images-1.medium.com/max/800/1*empw7x7T3FPKxddBsuMdnQ.png)

Note, we have created a platform channel using `MethodChannel()`, and then simply query it for the value. If we receive the value, we display as `_counter`, else, reset the `_counter` value to `-1`.

So, view a method as a async function invoked using `platform.invokeMethod` by its name, instead of signature. `platform` is the channel we created. Other than the way it is invoked, you may consider this as an async function.

### Codecs

Codecs are used to serialize and de-serialize data when crossing the boundary between Dart and native code. 

StandardMessageCodec is the default binary codec, and it supports basic data types (integers, doubles, strings, lists, and maps). If binary array is required, Uint8List can also be used.

As this is default, a channel with StandardMessageCodec can be created as below.

MethodChannel channel = MethodChannel('my_channel');

and the data can be passed as below. 

channel.invokeMethod('myMethod', {  
    'integerValue': 42,  
    'doubleValue': 3.14,  
    'stringValue': 'Hello, Native!',  
    'listValue': [1, 'two', 3.0],  
    'mapValue': {'key': 'value'},  
    'binaryData': Uint8List.fromList([0, 1, 2, 3]),  
  });  
channel.invokeMethod('myMethod', 100);  
channel.invokeMethod('myMethod', 3.14);  
channel.invokeMethod('myMethod', "Hello");  
channel.invokeMethod('myMethod', Uint8List.fromList([0, 1, 2, 3]));  
channel.invokeMethod('myMethod', [1, 'two', 3.0]);

BinaryCodec, StringCodec, JSONMessageCodec are some other codecs available.