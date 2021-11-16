const Logger = require('../utils/Logger');
const Overlays = require('../ui/Overlays');
const Eventing = require('../utils/Eventing');
const Const = require('../defs/constants');
const PlayerMedia = require('./PlayerMedia');
const PlayerUi = require('../ui/PlayerUi');
const AdsManager = require('../ui/AdsManager');
const FjError = require('../utils/FjError');
/**
 *  Class player in whinch the player is implemented
 */
class Player {
    constructor(fjID, vidContainerId) {
        this.logger = new Logger(this);
        this.playerPlaylist = null;
        this.playingList = false;
        this.loopingList = false;
        this.currentPlaying = -1;
        this.isPlaying = false;
        this.currentIsDash = false;
        this.playlistLoaded = false;
        this.playingAds = false;
        // default values
        this.videoWidth = '100%';
        this.videoHeight = '';
        this.events = new Eventing();
        this.videoContainerId = vidContainerId;
        this.fjPlayerId = fjID;
        this.OverlaysMgr = new Overlays();
        this.AdsMgr = new AdsManager(vidContainerId);
        this.supportsVideo = !!document.createElement('video').canPlayType;
        this.playerUi = new PlayerUi(this.videoContainerId, this.videoWidth, this.videoHeight);
        this.playerMedia = new PlayerMedia(this.fjPlayerId);
    }

    /**
     * function  to return a human redeable duration of secondes
     */
    static duration(secDuration) {
        const secNum = parseInt(secDuration, 10);
        let hours = Math.floor(secNum / 3600);
        let minutes = Math.floor((secNum - (hours * 3600)) / 60);
        let seconds = secNum - (hours * 3600) - (minutes * 60);
        if (minutes < 10) {
            minutes = `0${minutes}`;
        }
        if (seconds < 10) {
            seconds = `0${seconds}`;
        }
        if (hours === 0) {
            return (`${minutes}:${seconds}`);
        }
        if (hours < 10) {
            hours = `0${hours}`;
        }
        return (`${hours}:${minutes}:${seconds}`);
    }

    playItem(itemPosition, autostart) {
        let start = true;
        this.logger.info(`Start Playling Item  itemPosition : ${itemPosition}`);
        if (autostart !== true) {
            start = false;
        }
        this.currentPlaying = itemPosition;
        if (!this.playlistLoaded) {
            this.logger.error(' No playlist is loaded on player ');
            return false;
        }
        const item = this.playerPlaylist.getItem(itemPosition);
        if (item === null) {
            this.logger.error(' No item to play at index ', this.currentPlaying,
                ' playlist is sized ', this.playerPlaylist.getSize());
            return false;
        }
        // set title
        this.playerUi.setTitle(item[Const.FJCONFIG_TITLE], item[Const.FJCONFIG_SHOW_UP_TITLE]);
        // set share
        this.playerUi.setShareIcon(item[Const.FJCONFIG_SHARE]);
        // set down
        this.playerUi.setDownloadIcon(item[Const.FJCONFIG_DOWNLOAD]);
        // set back
        this.playerUi.setBackIcon(item[Const.FJCONFIG_BACK]);
        // set thumbs
        this.playerMedia.setThumbsUrl(item[Const.FJCONFIG_THUMBS]);
        // unload old
        this.playerMedia.Unload();
        // load new item
        if (item[Const.FJCONFIG_SRC] !== null || item[Const.FJCONFIG_SRC] !== undefined) {
            if (item[Const.FJCONFIG_TYPE] === Const.FJCONFIG_TYPE_DASH) {
                // clear dash
                this.currentIsDash = true;
                this.logger.warn(' will play a clear dash on caption obect ', this.playerUi.getVideoCaption());
                this.playerMedia.loadDash(
                    item[Const.FJCONFIG_SRC], item[Const.FJCONFIG_POSTER],
                    item[Const.FJCONFIG_SUBTITLES],
                    this.playerUi.getVideoCaption(), start, item[Const.FJCONFIG_DRM],
                );
            } else {
                this.playerMedia.load(item[Const.FJCONFIG_SRC], item[Const.FJCONFIG_TYPE],
                    item[Const.FJCONFIG_POSTER], item[Const.FJCONFIG_SUBTITLES], start);
            }
            return true;
        }
        this.logger.error('src of item is not valid , at index ', this.currentPlaying);
        return false;
    }

    playNext() {
        if (!this.playlistLoaded) {
            this.logger.error(' No playlist is loaded on player ');
            return false;
        }
        // set playlist again
        this.playingList = true;
        this.currentPlaying += 1;
        this.logger.log(' will play next', this.currentPlaying, ' in playlist is loaded on player ');
        if (this.playerPlaylist.getSize() < this.currentPlaying) {
            if (this.loopingList === true) {
                this.currentPlaying = 0;
            }
            // playlist if ended
            return false;
        }
        // play next
        this.playItem(this.currentPlaying);
        // auto play it
        this.playerUi.ShowVideo();
        this.playerUi.onplaypauseClick();
        return true;
    }

    AdsEventing(e, args) {
        this.logger.debug(' just a new event from this.AdsMgr ', e, args);
        // send Event to listener
        this.logger.warn('Sending Ads Event >>>>>>>>>>>>>>>>>   ', e);
        this.events.fireEvent(e);
        if (e === Const.AdsEvents.ADS_PLAYBACK_ENDED) {
            this.playingAds = false;
            if (args === Const.AdsEnum.ADS_PRE_ROLL) {
                if (this.AdsMgr.CheckPreAds() === true) {
                    return;
                }
                this.playerUi.ShowVideo();
                this.playerMedia.play();
                this.playerUi.toggleplaypauseBtn();
                return;
                // freezePlayer(false, true, false);
            } if (args === Const.AdsEnum.ADS_POST_ROLL) {
                if (this.AdsMgr.CheckPostAds() === true) {
                    return;
                }
                // check if in playlist then play list
                if (this.playingList === true) {
                    this.playerUi.toggleplaypauseBtn();
                    this.playerUi.ShowVideo();
                    this.playNext();
                }
                // freezePlayer(false, false, true);
            } else if (args === Const.AdsEnum.ADS_MID_ROLL) {
                this.playerUi.ShowVideo();
                this.playerMedia.play();
                this.playerUi.toggleplaypauseBtn();
                // freezePlayer(false, false, false);
            } else {
                this.logger.warn(' unknown Ads type !! ', args);
            }
        }
        if (e === Const.AdsEvents.ADS_PLAYBACK_STARTED) {
            this.playingAds = true;
            // hide the player and pause it
            this.playerMedia.pause();
            this.playerUi.hideVideo();
        }
    }

    midPlayingChecks(secondes) {
        this.OverlaysMgr.CheckOverlays(secondes);
        return this.AdsMgr.CheckMidAds(secondes);
    }

    playPrev() {
        if (!this.playlistLoaded) {
            this.logger.error(' No playlist is loaded on player ');
            return false;
        }
        // set playlist again
        this.playingList = true;
        this.currentPlaying -= 1;
        this.logger.log(' will play next', this.currentPlaying, ' in playlist is loaded on player ');
        if (this.currentPlaying < 0) {
            if (this.loopingList === true) {
                this.currentPlaying = this.playerPlaylist.getSize() - 1;
            }
            // playlist if ended
            return false;
        }
        // play next
        this.playItem(this.currentPlaying);
        // auto play it
        this.playerUi.ShowVideo();
        this.playerUi.onplaypauseClick();
        return true;
    }

    MplayerEventing(e, args) {
        let item; let
            vid;
        if (e === Const.PlayerEvents.PLAYBACK_TIME_UPDATE) {
            this.playerUi.UpdateProgress(this.playerMedia.time());
            vid = this.playerUi.getVideo();
            this.playerUi.setDuration(this.playerMedia.getDuration());
            this.midPlayingChecks(Math.round(this.playerMedia.time()));
        } else {
            if (e === Const.PlayerEvents.PLAYBACK_ENDED) {
                this.isPlaying = false;
                if (this.AdsMgr.CheckPostAds() === true) {
                    this.logger.debug('starting  post ads !!');
                } else if (this.playingList === true) {this.playNext();}
            }
            if (e === Const.PlayerEvents.PLAYBACK_PAUSED) {
                this.isPlaying = false;
            }
            if (e === Const.PlayerEvents.PLAYBACK_STARTED) {
                // first starting  only
                if (args === 1) {
                    this.isPlaying = true;
                    if (this.AdsMgr.CheckPreAds() === false) {
                        this.playerMedia.play();
                    } else {
                        this.playerMedia.pause();
                    }
                }
                this.playerUi.HideSpinner();
                this.playerUi.toggleplaypauseBtn();
                this.playerUi.setDuration(this.playerMedia.getDuration());
            }

            if (e === Const.PlayerEvents.STREAM_LOADED) {
                if (this.isPlaying === false) {
                    this.logger.warn(' Already Playing ...............');
                    this.playerUi.ShowSpinner();
                }
                // checks thumbs
                this.playerUi.SetupThumbsManager(this.playerMedia.getDuration(), args);
                // set subsgetTextTracks()
                this.playerUi.SetupSubsAudsManager(this.playerMedia);

                this.playerUi.setDuration(this.playerMedia.getDuration());
                item = this.playerPlaylist.getItem(this.currentPlaying);
                // Set Overlays
                this.OverlaysMgr.Setup(item[Const.FJCONFIG_OVERLAYS]);
                // Set ads
                vid = this.playerUi.getVideo();

                this.AdsMgr.Setup(item[Const.FJCONFIG_ADS], vid.videoWidth, vid.videoHeight);
            }
            if (e === Const.PlayerEvents.PLAYBACK_SEEKING) {
                this.isPlaying = false;
                this.playerUi.ShowSpinner();
            }
            if (e === Const.PlayerEvents.PLAYBACK_SEEKED) {
                this.isPlaying = true;
                this.playerUi.HideSpinner();
            }

            // send Event to listener
            if (typeof e !== 'undefined') {
                this.logger.info('[Event] [trigger] > ', e);
                this.events.fireEvent(e);
            }

            if (e === Const.PlayerEvents.PLAYBACK_ERROR) {
                this.playerUi.goForError();
                throw new FjError(args.code, args.type, args.message,
                    document.getElementById(this.playerUi.getErrorDivId()));
            }
        }
    }

    /**
     *
     */
    loadPlaylist(playlist) {
        this.logger.log(' start  function ');
        if (!this.supportsVideo) {
            this.logger.error(' browser did not support video !');
            return false;
        }
        if (playlist.getSize() > 0) {
            this.playerPlaylist = playlist;
            this.playlistLoaded = true;
            this.playerUi.initialize(this);
            this.playerMedia.on(Const.PlayerEvents.TRACKS_ADDED, (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.STREAM_LOADED, (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_STARTED,
                (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_ERROR, (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_PAUSED, (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_ENDED, (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_SEEKED, (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_SEEKING,
                (e, a) => this.MplayerEventing(e, a));
            this.playerMedia.on(Const.PlayerEvents.PLAYBACK_TIME_UPDATE,
                (e, a) => this.MplayerEventing(e, a));

            this.AdsMgr.on(Const.AdsEvents.ADS_PLAYBACK_STARTED, (e, a) => this.AdsEventing(e, a));
            this.AdsMgr.on(Const.AdsEvents.ADS_PLAYBACK_ERROR, (e, a) => this.AdsEventing(e, a));
            this.AdsMgr.on(Const.AdsEvents.ADS_PLAYBACK_ENDED, (e, a) => this.AdsEventing(e, a));

            this.playerMedia.initialize(this.playerUi.getVideo());
            this.OverlaysMgr.initialize(
                document.getElementById(this.playerUi.getOverlaysContainerDivId()),
            );
            this.AdsMgr.initialize(document.getElementById(this.playerUi.getAdsContainerDivId()));
            return true;
        }
        this.logger.error(' playlist is empty: ', playlist.getSize());
        this.playlistLoaded = false;
        return false;
    }

    /**
     *
     */
    playAt(index, autostart) {
        let start = true;
        if (autostart !== true) {
            start = false;
        }
        this.playingList = false;
        return this.playItem(index, start);
    }

    startPlaylist(positionToStartFrom, loop, randomPlay, autostart) {
        let start = true;
        if (autostart !== true) {
            start = false;
        }
        this.currentPlaying = positionToStartFrom;
        if (!this.playlistLoaded) {
            this.logger.error(' No playlist is loaded on player ');
            return false;
        }
        const item = this.playerPlaylist.getItem(this.currentPlaying);
        if (item === undefined) {
            this.logger.error(' No item to play at index ', this.currentPlaying,
                ' playlist is sized ', this.playerPlaylist.getSize());
            return false;
        }
        this.playingList = true;
        this.loopingList = loop;
        // set title
        this.playerUi.setTitle(item[Const.FJCONFIG_TITLE], item[Const.FJCONFIG_SHOW_UP_TITLE]);
        // set share
        this.playerUi.setShareIcon(item[Const.FJCONFIG_SHARE]);
        // set down
        this.playerUi.setDownloadIcon(item[Const.FJCONFIG_DOWNLOAD]);
        // set back
        this.playerUi.setBackIcon(item[Const.FJCONFIG_BACK]);
        // set thumbs
        this.playerMedia.setThumbsUrl(item[Const.FJCONFIG_THUMBS]);
        // play item
        if (item[Const.FJCONFIG_SRC] !== null || item[Const.FJCONFIG_SRC] !== undefined) {
            if (item[Const.FJCONFIG_TYPE] === Const.FJCONFIG_TYPE_DASH) {
                // clear dash
                this.currentIsDash = true;
                this.playerMedia.loadDash(
                    item[Const.FJCONFIG_SRC],
                    item[Const.FJCONFIG_POSTER],
                    item[Const.FJCONFIG_SUBTITLES],
                    this.playerUi.getVideoCaption(), start, item[Const.FJCONFIG_DRM],
                );
            } else {
                this.playerMedia.load(item[Const.FJCONFIG_SRC], item[Const.FJCONFIG_TYPE],
                    item[Const.FJCONFIG_POSTER], item[Const.FJCONFIG_SUBTITLES], start);
            }
            return true;
        }
        this.logger.error('src of item is not valid , at index ', this.currentPlaying);
        return false;
    }

    seek(time) {
        this.playerMedia.seek(time);
    }

    reset() {
        this.playerMedia.Unload();
        this.playerUi.reset();
    }

    play() {
        this.playerMedia.pause();
        if (this.AdsMgr.CheckPreAds() === false) {
            this.playerMedia.play();
        }
        this.playerUi.toggleplaypauseBtn();
    }

    pause() {
        this.playerMedia.pause();
        this.playerUi.toggleplaypauseBtn();
    }

    isPlayingAds() {
        return this.playingAds;
    }

    isReady() {
        return this.playlistLoaded;
    }

    isPaused() {
        return this.playerMedia.isPaused();
    }

    isEnded() {
        return this.playerMedia.isEnded();
    }

    /**
     *
     */
    on(name, handler) {
        return this.events.on(name, handler);
    }

    /**
     *
     */
    off(name, handler) {
        return this.events.off(name, handler);
    }
}
module.exports = Player;
