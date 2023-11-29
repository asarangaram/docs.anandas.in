I am using [Hugo](http://gohugo.io/) to develop webpages. [Homebrew / LinuxBrew](https://brew.sh) Installation was required for keeping [Hugo](http://gohugo.io/) version upto date. According to [Hugo's document](https://gohugo.io/getting-started/installing#debian-and-ubuntu),  the Hugo in Linux package managers for Debian and Ubuntu is usually a few versions behind, so notr a recommended method.

# To install:
```
sudo apt-get install build-essential
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> .bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install gcc
```

# Install Hugo
```
brew install hugo
```

