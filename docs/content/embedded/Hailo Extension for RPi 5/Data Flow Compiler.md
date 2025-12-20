
In this article, let us go deep into how to get AI models (pre-trained),  convert it into .hef (Hailo Executable File.) and use it with Hailo-8 HAT for RPi. I have avoided optimised implementations for making this article simple. 

We don't use any GPU, but require a linux machine to run Hailo DFC (Data Flow Compiler).

To make this understandable, I have used image similarity search as an example through out this discussion.

## Terminologies


## Finding pre-trained AI models.

What are the options available to view the ONNX files?

### Netron
Install netron
```
pip install netron
netron <model>.onnx
```

This servers the model on a web-server which you can open on any browser. If you are running on a headless server, redirect the port so that you can open. There are many ways, but I prefer the following way.
* ssh to server with port forwarding.
```

```



## Parsing with hailo parser
```
hailo parser onnx  cas_vit_m.onnx
```