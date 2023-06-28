---
title: Image Repo as a Flask Microservice
weight: 551000
---

# `Image Repo` as a Flask Microservice

In this tutorial, our goal is to create a Flask Microservice that enables image uploading, archiving, and gathering information about the images. This will be achieved by extracting metadata and performing image analysis. To define endpoints, we will utilize REST APIs implemented with `flask_restful`. As we progress through the tutorial, we will enhance the implementation and incorporate additional features in each chapter.

The main objective of this product is to establish a self-hosted server within a home network or intranet, utilizing Free and Open-Source Software ([FOSS](https://en.wikipedia.org/wiki/Free\_and\_open-source_software)). Initially, we will execute the entire process on a Linux machine and later configure a _Raspberry Pi_ to replace it as the server. Additionally, we will develop a [Flutter](https://flutter.dev/)-based app to serve as a sample front-end for utilizing this microservice. It's important to note that the primary focus is on the microservice provided through the REST API, rather than the app itself. Therefore, the app will feature a simple user interface solely designed to demonstrate the usage of the API. This service can be hosted and utilized within any application requiring similar functionalities.

{{% children depth="1"  %}}
