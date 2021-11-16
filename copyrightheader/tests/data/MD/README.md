# **fjplayer** #

## What is fjplayer ##

* it's a 100 % customiazble video player base on html 5 video Player
* it's support dash and mp4 sources
* it support multi subs tracks
* it support overlays ads and any information overlays
* it support injection mp4 video ads in preroll,modroll or after rolling main video
* based on sdhakla player

## Using fjplayer ##

### include fjplayer file ##
  **dist/fjplayer.js** for fjplayer styles and javascript code , no other dependecies is needed

```html
<script type="text/javascript" src="/dist/fjplayer.min.js"></script>
```

### html  ###
In your html code , you need to add a div with a an Id to be used bu the player

```html
<div id="playercontainer">
</div>
```

### java script coding ###
In order to create a player and use , we need to create a playlist first :
 ```javascript
var playlist = new fjplayer.Playlist();
```
Then specify one or more elements and add them to the playlist

```javascript
    var forjaItemDashEncryptedWithPreAds = {
         'FJType': 'dash',
         'FJTitle': 'clear Forja movie itemDash ',
         'FJClass': 'vod',
         'FJSrc': 'http://127.0.0.1:8500/dashedCrypted/stream.mpd',
         'FJDrm': {
             "FjLicenseServer": "http://127.0.0.1:3000"
         },
         'FJAds': [{
             'FJType': 'video/mp4',
             'FJSrc': '../videos/berber_pub.mp4',
             'FJClass': 'pre-roll',
             'FJCanEscape': true,
             'FJUrl': 'http://www.google.com'
         }]
     };
    var Mp4SubsWithThumbs = {
         'FJSrc': 'https://content.jwplatform.com/videos/q1fx20VZ-kNspJqnJ.mp4',
         'FJTitle': ' title of movie itemOnly 1',
         'FJClass': 'vod',
         'FJThumbs': '../vtt/thumbs.vtt',
         'FJType': 'video/mp4',
         'FJSubtitles': [{
             'FJLabel': 'English',
             'FJLang': 'en',
             'FJSrc': '../vtt/sintel-en.vtt'
         }, {
             'FJLabel': 'Espagnol',
             'FJLang': 'es',
             'FJSrc': '../vtt/sintel-es.vtt'
         }, {
             'FJLabel': 'Deutsch',
             'FJLang': 'de',
             'FJSrc': '../vtt/sintel-de.vtt'
         }]
     };
   var clearSteam = {
         'FJType': 'dash',
         'FJTitle': 'clear Forja movie itemDash ',
         'FJClass': 'vod',
         'FJSrc': 'http://127.0.0.1:8500/bclear/stream.mpd'
     }

     playlist.addItem(Mp4SubsWithThumbs);
     playlist.addItem(clearSteam);
```

Now , you can create player where first argument is the playerKey and the second is the id of the div container in html  and load the playlist;
```javascript
var player = new fjplayer.Player('fjserverID1', 'playercontainer');
player.loadPlaylist(playlist);
```

You can also add event listener ;
```javascript
   function fjplayerEvent(e, args) {
            console.warn(" We are having an event : ", e, args);
        };
   player.on(fjplayer.PlayerEvents.STREAM_LOADED, fjplayerEvent);
```
finally, you can start playing , in this example we start play at element 0, looping is true , random play id false and autostart is true ;
```javascript
player.startPlaylist(0, true, false, true);
```

### developping fjplayer  ###
after doing :
* npm install : to install dependecy
* npm run live : to run http demo and developiong watching mode for javascript code

demo app will be launched at http://localhost:8080


### Playlist Item ###

A Playlist item will contains theses  elements :

| item field        | mandatory |     value                     |  Description     |
|-------------------|-----------|-------------------------------|---------------|
| FJClass           |  YES      | 'vod' or 'live'               | the class of the stream |
| FJType            |  YES      | 'video/mp4' or 'dash'         | the type of the stream|
| FJTitle           |  YES      | non empty string              | the title to be shown when playing|
| FJSrc             |  YES      | non empty url string          | the url of the stream to be played|
| FJDownload        |  NO       | non empty url string          | activate download icon and open new  widown on url when icon is clicked|
| FJShare           |  NO       | non empty url string          | activate share icon and open new  widown on url when icon is clicked|
| FJBack            |  NO       | non empty url string          | activate back arow icon and locate current window to url when icon is clicked|
| FJUpTitle         |  NO       | boolean                       | show of not the title in player up|
| FJSrc             |  YES      | non empty url string          | the url of the stream to be played|
| FJDrm             |  NO       | integer                       | it's an object containing drm security information|
| FJPoster          |  NO       | url to image poster           | url to poster to be showing wen loading |
| FJThumbs          |  NO       | url to image thumbs           | url to file containing tooltip thumbnail images for video associated with WebVTT  : to generate this file you can visit  [github video scripts](https://github.com/vlanard/videoscripts) |
| FJSubtitles       |  NO       | array of subtitles Items      |
| FJAds             |  NO       | array of video ads Items      |
| FJOverlays        |  NO       | array of overlays Items       |

### fjplayer  *ads* ###
The object ads , must be inserted on array **FJAds** under item on playlist.
The Ads  is referring to advertissment.
When it's time to play this ads , fjplayer will  pause main video hide the controls , play the Ads and show a transparent banner up on which the countdown timer before the ads ends.

Ads  also contains :

| ads item  field    | mandatory |     value              |  Description     |
|-------------------|-----------|-----------------------|---------------|
| FJType            |  YES      | 'video/mp4' or 'dash'         | the type of the stream|
| FJSrc             |  YES      | non empty url string          | the url of the stream to be played|
| FJClass           |  YES      | 'pre-roll' , 'mid-roll' or 'post-roll' | pre: before main video, mid: in the middle and post: after the main video |
| FJCanEscape         |  YES         | boolean    |  display a button to escape ads or not   |
| FJFJUrlSrc             |  YES      | non empty url string          | the url of the advertiser, when user click on video when ads playing , a windows will be opened on this url|
| FJShowAt     |  YES (mid-roll)         | integer                | the number of seconds use to start the Ads if it mid-roll class|

if  **FJShowAt** is negatif or bigger than ads duration , then the concerned ads wil not be player.

### fjplayer  *subtitle* ###
The object  subtitle , must be inserted on array **FJSubtitles** under item on playlist.
It permit to add a webvtt subtitles other that existing in mpd (in case of dash ) .
it  contains :

| subtitle   field    | mandatory |     value              |  Description     |
|-------------------|-----------|-----------------------|---------------|
| FJLabel         |  YES         | non empty string        | string label of subtitles to be shown on control |
| FJSrc              |  YES         | non empty url string    | url of the web vtt subtitles file |
| FJLang          |  YES         | fr or en or de ...     | ISO descripton of language |

### fjplayer *overlay* ###
The object overlay , must be inserted on array **FJOverlays** under item on playlist.
An overlay is a graphic layer above the video layer that conatains data like ads data.
When user lick on an overlay a new opened will be opened with the  url **FJOverUrl**.
Ii will be showing at **FJOverShowAt** and for a duration of **FJOverDuration** .
If **FJOverShowAt** or **FJOverShowAt**+**FJOverDuration** is bigger than the item movie duration, then the overlays will not be schown at all .
it  contains :

| overlay   field    | mandatory |     value              |  Description     |
|-------------------|-----------|-----------------------|---------------|
| FJData         |  YES         | non empty string        | html data that will be putted on div overlay |
| FJUrl         |  YES         | non empty url string    | url to open in new window to when the user click on overlay |
| FJDuration     |  YES         | integer                | in seconds , the duration of overlay show |
| FJShowAt      |  YES         | integer                 | in seconds , the time in video to start to schow the overlay  |

### fjplayer *drm* ###
*This part of specs is not supported yet by player*
The object drm   , is referring to Digital right managment and it's contains data about media drm .
This object is managed onlywhen **FJType** is *dash* .
It must be in **FJDrm** field
it  contains :

| drm   field                    | mandatory |     value                              |  Description     |
|-------------------------------|-----------|---------------------------------------|---------------|
| FJDrmScheme                    |  YES         | 'forja','playReady,'clearKey' or 'widevine'     | drm Scheme to use  |
| FJLicenceServer                |  YES         | non empty url string                    | url of the Licensing server |
| FJHeadersOnLicenseRequest     |  NO         | object contains headers and value     | headers and value to be add to request when asking for license |
| FJHeadersOnSegmentsRequest     |  NO         | object contains headers and value     | headers and value to be add to request when asking for segment |

The Drm scheme **fjserver** is a clear key based scheme done on **fjserver** .
