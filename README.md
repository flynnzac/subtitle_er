This script uses OpenAI's whisper library to generate mpsub-formatted subtitles for a video.

It can be used as a library or as a script. As a script:

```
python3 subtitle_er.py VIDEO_FILE VIDEO_TITLE [CHANGE_EVERY] [MODEL_NAME] > subtitles.mpsub 
```

`VIDEO_FILE` is the path to the video file.

`VIDEO_TITLE` is the title to use for the video

`CHANGE_EVERY` is the approximate number of seconds to leave subtitles on the screen before switching to the next subtitles. It is optional. If omitted, 5.0 seconds will be used which I've found usually feels natural.

`MODEL_NAME` is the model name to use. If omitted, "base" is used, which generally works well.

The script prints the subtitle file to standard output so redirect to a file to save.

To play with `mplayer` use:

```
mplayer VIDEO_FILE -sub SUBTITLE_FILE
```


