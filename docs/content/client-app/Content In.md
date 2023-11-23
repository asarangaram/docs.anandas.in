# Content - In
This article discusses various aspects of loading content in an *Application*.

## Content
 `content` can exist in various forms, such as text, image, video, or audio. Except for text, the remaining three are collectively referred to as media. Text can be in plain form (encoded with a standard character set) or in a formatted form within a container. Media always comes within a container. This container, which holds any type of content, is generally called a file and is identified by a URI (Uniform Resource Identifier).

Therefore, content can be obtained either as plain text (`text/plain`) or within a container identified by a URI, which is again a string of characters or text (`text/uri`). The `text/uri` is used to query and fetch the content, which can be either `text/plain` or `binary`.

## Application (`app`)

An application is a program designed to execute a specific set of tasks for the end user. In any given task, the application loads/creates content, processes the content, and shares/saves the content.

The `app` can either create or load content. Text-based content can be directly entered via keyboards, while other content can be generated using available sensors (such as a camera or microphone). Content generated from other sensors is typically encoded as `text/plain` or `binary`.

The `app` is also capable of receiving content from another app or reading from either local storage or the network. Based on predefined algorithms and user interaction through pointing devices (mouse, touch sensors, etc.), the content is processed or converted into another form.

The processed content is then presented via available output sensors (display, speaker, etc.) or shared with another app, or it can be sent to local storage or the network.

There are many sensors to input content, present content as well to interact with the application. 

### Load Content

Content is loaded when the user pushes it from another application or explicitly loads it from local storage (file system or local database) or the network by providing an appropriate URI.  Commonly used User Interface (UI) features that facilitate the input or transfer of content into an application include:

1. Share
2. Drag and Drop
3. Copy and Paste
4. Import / Download

	Note that recording and keying-in are mechanisms that create content directly and are not grouped with the concept of 'Loading Content'.

Most of the explicit mechanisms could be categorized into either of the above four groups.

Additionally, there are implicit mechanisms by which content is loaded into the application, achieved by registering for content delivery / Monitoring.  They are usually implemented by register once and get the content either periodically or when available /changed.

1. Watch / monitor / auto-sync
2. Data base triggering 
3. Automatic load when the app starts



| pub dev search word | purpose | comments|
|---|---|---|
| receive+intent | to register and accept the content shared from other applications |The sharing functionality is integrated into the Mobile platforms' Operating System and commonly used by Mobile Apps. This concept is friendly to touch interfaces. On Desktop Operating Systems, this concept is usually integrated into context menu as 'send'. There are attempts to have share button on latest desktop applications too. |
| drag and drop | to select items in an app, drag and drop them into another app| This concept is good for devices supporting point device with DnD functionality. They are commonly used in Desktop application, as they have bigger screens that helps to view more than one application simultaneously. While drag and drop concept is available in Mobile apps, they are usually works within the app. There are ways to implement this method on mobile devices with bigger screens / supports screen split.  |
| copy and Paste<br/>clipboard | to copy content from an app and paste it into another using operating systems clip board.| Copy and paste are usually provided in all kind of devices, either with pop up menus or context menus or with overloading the touch gestures or pointing device actions. |
| Import / download| to invoke a object selector (file browser / DB viewer) and allow user to select and accept the content interactively | All operating systems provide mechanism for this| 


## DropItIn

What if all the explicit methods are provided by a single package for Flutter applications? This is what being done in this package, `DropItIn`.  The approach is not to implement everything from the scratch but to use the existing packages as much possible either as it is and provide a wrapper or modify to support some missing parts.



Flutter provides limited in-built mechanism and most of the mechanism provided are as plugins. The objective of this package (DropItIn) is to make all the above methods available as set of Flutter widgets.

Here is the list of popular packages and their purpose, along with some comments.
