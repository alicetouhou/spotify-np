# spotify-np
Spotify module for polybar using the spotify API


[![Ex1](http://benji42.u.catgirlsare.sexy/TEMq.png)](http://benji42.u.catgirlsare.sexy/TEMq.png)

[![Ex2](http://benji42.u.catgirlsare.sexy/X_3F.png)](http://benji42.u.catgirlsare.sexy/X_3F.png)

# Dependencies
- Python 3
- Python `spotipy` module
- Python `requests` module
- Python `wcwidth` module

# Setup
### Install Dependencies
Ubuntu:
```
sudo apt-get update
sudo apt-get install python3
sudo apt install python3-pip
pip3 install spotipy
pip3 install requests
pip3 install wcwidth
```
### Create application in spotify
1. Go to https://developer.spotify.com/dashboard/ and sign in.
2. Click "Create an App". Don't worry about the name, description, or what you're building. This information can be anything but I'd make to make it something you can remember in the future.
3. Open the app and click on settings. Add `http://localhost:7777/callback` into the Redirect URIs.
4. Stay on this page. You'll need it for the setup later.

### Add the module to polybar
Before adding the module, move `spotify_np.py` to a folder and set `path/to/script.py` to the location of this file.
~~~ ini
[module/spotify-np]
type = custom/script
interval = 0
tail = true
format = <label>
exec = python3 path/to/script.py [arguments]
~~~
and add the `spotify-np` module to the bar you'd like to display the information on.

### Arguments
#### Userinfo (-i)
Used to connect your module to your spotify account. Necessary for the module to function. Both the client ID and client secret are in the page for the application you created earlier.

Syntax: `username, client ID, client secret`

Example:
~~~ini
exec = python3 path/to/script.py -i awesomeuser16,ILVGVkzXNSZZVl62Ez1IooYA75RdaOY0,CTL6hA8nmhJ3QqWf7jsQmXWf8QvOtX7e
~~~
#### Format (-f)
Format of the module in polybar.

Information to output:
`volume` , `progress` , `duration` , `bar` , `time_left` , `artist` , `title` , `track_number` , `disc_number`

Example:
~~~ini
exec = python3 path/to/script -f '{volume}% | {progress} {bar} {duration} | {artist} - {title}'
~~~
This will output "61% | 3:16 ----------|----- 4:44 | Mogwai - 20 Size", as shown in the screenshot.

Default: `'{progress} / {duration} | {artist} - {title}'`

#### Maxlength and Minlength (-l and -m)
Length of the module in polybar.

Example:
~~~ini
exec = python3 path/to/script.py -l 35 -m 35
~~~
Default: `50`

### Barlen (-b)
Length of the progress bar in polybar.
Example:
~~~ini
exec = python3 path/to/script.py -b 20
~~~
Default: `16`

### Reload Polybar
After reloading, you should be brought to a webpage to authorize a spotify application. Give the application authorization and it should work as soon as you play a new song on spotify.
