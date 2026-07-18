### Markdown Browser — A Flutter Package

Recently I came across a tweet asking how to publish user manuals inside a Flutter application. The suggestions were either to use web view or markdown. Compare to web view approach, the markdown approach is impressive. 

The advantages I found are

1. You can make a markdown server very quickly and doesn’t require complex setup. (Check the server section below)
2. Its faster to create content in markdown format.

However, while checking over [pub.dev](https://pub.dev/), I could find packages that displays markdown files, but none to browse across markdown files, assuming the files share same URL prefix. While it looks easier to make, having a package might help the app developers to quickly integrate. 

I would not recommend creating a package for every minor issue. However, this seems to be a common problem that could benefit many developers. Hence decided to make a package. 

### Requirements

There are a couple of general requirements.

1. The user manual should be divided into multiple markdown files, with seamless navigation between them.
2. The Markdown pages may include external links, which the app developer may want their users to open in their preferred browser or as a web view.
3. You should be able to utilize as many of the markdown features as possible.
4. The app developer should have some control over the content’s appearance, particularly in terms of fonts and colors.
5. Some manuals may feature diagrams and equations, and supporting these elements will contribute to creating better documentation.
6. Application should be able to point directly to any page based on the context, instead of always redirecting to the home page.

#### Balancing Act: External Packages vs. Building from Scratch

I have found a couple of mature packages that are readily available for displaying Markdown. Opting for these packages would significantly reduce development and testing efforts. However, it’s worth noting that each one comes with its own set of limitations, which would require additional work to overcome in order to support all desired Markdown features.

After reading the documentation of various markdown packages, I finalized [markdown-widget](https://pub.dev/packages/markdown_widget)

The key reasons are

1. It has table of content feature
2. Supports “Select all” and “Copy”
3. Allows extension to support new HTML tags / markdown blocks
4. Possible to override the behavior for existing markdown blocks.

#### State Management

The browser is required to download multiple markdown files and allow seamless navigation between them. This necessitates the development of a browser with support for saving history.

Users may frequently revisit the same page, and the app should efficiently avoid redundant content downloads. These requirements highlight the need for effective state management.

I opted for Riverpod due to its intuitively simple design for state management. Utilizing StateNotifierProvider facilitates easy implementation of navigation and history management, while FutureProvider streamlines content downloads.

I refrained from using any specific Navigator as users may wish to embed the user manual within a page, particularly in a Desktop environment. Additionally, there’s a possibility that users might prefer alternative page routers, potentially causing integration conflicts. Having the user manual as a widget offers more versatility in these scenarios.

#### Navigation bar

The browser requires a navigation bar, that allows to navigate back in history, and return to the main page from where the user started reading the manual. 

Few requirements for navigation bar are

1. The navigation bar should have minimum buttons.
2. it should not hinder the reading, preferably vanish when user starts reading.

### Implementation

I started the implementation by keeping the markdown files as assets. We need many markdown files to start with the development. ChatGPT became handy in this situation. A simple prompt to create many interlinked files with different markdown features with [Lorem Ipsum](https://www.lipsum.com/) text made creating the content for development quicker and easier.

#### Server

As the browser is expected to work for both offline and online manual, I quickly developed a Flask server that can serve the markdown files from a folder.

This is dead simple, and requires less that 25 lines of code and can be started with another bash script given below

from flask import Flask, send_from_directory  
import os  
  
# Flask app  
app = Flask(__name__)  
  
# Define the folder where markdown files are stored  
markdown_folder = 'online_user_manual'  
  
@app.route('/')  
def index():  
    # List all available markdown files - used to create a Dynamic TOC  
    markdown_files = [f for f in os.listdir(markdown_folder) if f.endswith('.md')]  
    return '\n'.join([f'<a href="/{filename}">{filename}</a>' for filename in markdown_files])  
  
@app.route('/<path:filename>')  
def serve_markdown(filename):  
    # Serve the requested markdown file  
    return send_from_directory(markdown_folder, filename)  
  
if __name__ == '__main__':  
    app.run()

#! /bin/bash  
  
V_ENV=".venv"  
  
if [ ! -d "$V_ENV" ]; then  
    echo "$V_ENV does not exist. Creating"  
    python3 -m venv .venv  
fi  
  
source "${V_ENV}/bin/activate"  
pip install flask  
flask --app server.py run -h 0.0.0.0  
deactivate

now, this will serve the files in a intranet server at port 5000.

> [http://x.x.x.x:5000](http://x.x.x.x:5000)

You may use any other framework, but need to ensure that all the files are served under same prefix.

#### Define the Package Interface

In the first version, I defined a very simple interface, with only three parameters. 

  const MarkdownBrowser({  
    super.key,  
    required this.urlBase,  
    this.landingPage,  
    required this.onExitCB,  
  });

- `urlBase`: This is the prefix for the markdown files. If the files are stored offline, it could be a path prefix from the asset folder. If the files are hosted online, should be a standard URL starting with either `http://` or `[https://](https://.)`[.](https://.)
- `landingPage`: This refers to the initial markdown file that the user needs to view within the given context.
- `onExitCB`: This is a callback function that allows the application to request the closure of the browser.

This version did not support any customization and utilized an internal page downloader. At this stage, I was unsure about the specific customization requirements, as I am new to the parent package (`markdown_widget`). Additionally, there were no customer specifications provided for customization.

#### Model

A Model class is defined to represent a markdown file within a specific context, as declared below. This class represents a point in the history to which the user has navigated.

class MarkDownFile {  
  final String urlBase;  
  final String landingPage;  
  final bool isOnline;  
  final String? currentSection;  
  
  MarkDownFile({  
    required this.urlBase,  
    required this.landingPage,  
    this.currentSection,  
  }) : isOnline =  
            urlBase.startsWith("http://") || urlBase.startsWith("https://");  
  
  MarkDownFile copyWith({String? landingPage, String? currentSection}) {  
    return MarkDownFile(  
      urlBase: urlBase,  
      landingPage: landingPage ?? this.landingPage,  
      currentSection: currentSection ?? this.currentSection,  
    );  
  }  
  
  String get path => "$urlBase/$landingPage";  
  
  MarkDownFile newPage({required String landingPage, String? currentSection}) {  
    return copyWith(landingPage: landingPage, currentSection: currentSection);  
  }  
  
  @override  
  String toString() {  
    return 'MarkDownFile(urlBase: $urlBase, landingPage: $landingPage, isOnline: $isOnline, currentSection: $currentSection)';  
  }  
}

#### Providers

I was in need for two StateNotifierProviders to manage the navigation and one FutureProvider to download the content.

**StateNotifierProvider**

s_currentFileProvider_ provides a _MarkDownFile_ object that is visible to the user and _historyProvider_ maintains a stack of _MarkDownFile_ objects. Both uses state notifiers to update when changed.

Both these providers are implemented such that they are available only inside the package, with overrides when the API is called by the application. 

I am using this approach to prevent the application and other modules use these providers without appropriate context. If you are a Flutter developer, please make me aware if this usage is incorrect.

final MarkDownFile pageDescriptor =  
        MarkDownFile(urlBase: urlBase, landingPage: landingPage ?? "index.md");  
    return ProviderScope(  
      overrides: [  
       currentFileProvider  
            .overrideWith((ref) => CurrentFileNotifier(pageDescriptor, ref)),  
       historyProvider.overrideWith((ref) => HistoryNotifier()),  
      ],  
      child: BrowserView(  
        onExit: onExitCB,  
      ),  
    );

The implementation of notifier and provider is as below. Note the implementation of pop() and home() in HistoryNotifier to navigate back in the history and reset the history to go back to the first file visited (respectively).

class CurrentFileNotifier extends StateNotifier<MarkDownFile> {  
  final List<MarkDownFile> history = [];  
  final Ref ref;  
  
  CurrentFileNotifier(MarkDownFile pageDescriptor, this.ref)  
      : super(pageDescriptor);  
  
  void newPage({required String landingPage, String? currentSection}) {  
    state =  
        state.newPage(landingPage: landingPage, currentSection: currentSection);  
  }  
}  
  
final currentFileProvider =  
    StateNotifierProvider<CurrentFileNotifier, MarkDownFile>((ref) {  
  throw Exception(  
      "currentFileProvider is available only inside the markdown_browser");  
});  
  
class HistoryNotifier extends StateNotifier<List<MarkDownFile>> {  
  HistoryNotifier() : super([]);  
  
  push(MarkDownFile file) {  
    state = [...state, file];  
  }  
  
  MarkDownFile? pop() {  
    if (state.isNotEmpty) {  
      final file = state.last;  
      state.removeLast();  
      return file;  
    }  
    return null;  
  }  
  
  MarkDownFile? home() {  
    if (state.isNotEmpty) {  
      final file = state.first;  
      state = [];  
      return file;  
    }  
    return null;  
  }  
}  
  
final historyProvider =  
    StateNotifierProvider<HistoryNotifier, List<MarkDownFile>>((ref) {  
  throw Exception(  
      "historyProvider is available only inside the markdown_browser");  
});

**FutureProvider**

FutureProvider is the simplest way to manage external resources, such as content downloading or file loading, which are inherently asynchronous. It returns an `AsyncValue` object to the widgets that are listening. This allows for elegant handling of waiting and error scenarios. Additionally, using the `.family` modifier enables the creation of multiple providers based on external parameters, in our case _path._

Future<String> getMarkdownFile(String path) async {  
  final nwFile = path.startsWith("http://") || path.startsWith("https://");  
  if (!nwFile) {  
    try {  
      return await rootBundle.loadString(path);  
    } on Exception {  
      throw Exception("Error loading asset  $path.\nCheck if file exists.");  
    }  
  } else {  
    final uri = Uri.parse(path);  
  
    Response response = await get(uri).timeout(const Duration(seconds: 5));  
    if (response.statusCode == 200) {  
      return response.body;  
    } else {  
      throw Exception(  
          "Error Downloading $path.\nError code: ${response.statusCode.toString()}."  
          "\nCheck if the server is reachable\nand the file exists");  
    }  
  }  
}  
  
final markdownFileProvider =  
    FutureProvider.family<String, String>((ref, path) async {  
   
  return getMarkdownFile(path);  
});