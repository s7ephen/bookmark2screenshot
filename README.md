# bookmark2screenshot
Browse your bookmarks as screenshots.
Go from a bookmarks file to galler of screenshots of the bookmarks.

More info on the [WIKI](https://github.com/s7ephen/bookmark2screenshot/wiki)

|From this | To This | 
|-|-|
|![bookmarks](https://github.com/s7ephen/bookmark2screenshot/wiki/media/884f29d1f88648fbb75c38ba0bc74337.png)|![nytthing](https://github.com/s7ephen/bookmark2screenshot/wiki/media/8d419c30c593405aa5459f9ccc29523b.png)|


# demo
![thing](https://github.com/s7ephen/bookmark2screenshot/wiki/media/bookmark2screenshot_gallery_demo_4x_much_lowerrez.gif)

Files:
|File | Description | 
|-|-|
|`bookmark2screenshot_gallerymaker.sh`| Script to download and execute the gallerymaking container (optional)
|`bookmark2screenshot.py`| The main thing. but woefully needy. Needs to be containerized, but it is so needy, that its needs have more needs. I have not yet found a way to make it stop complaining when i put it in a docker prison.|
|`Dockerfile`| the source Dockerfile for this container https://hub.docker.com/r/sa7ori/bookmark2screenshot_gallerymaker cuz Docker doesnt bundle the source file in the container and is dumb like the Howard Rourke's columns on the Parthenon|

