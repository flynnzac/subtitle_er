import whisper
import sys

def add_word(state, word):
    word_time = word["end"] - word["start"]
    state["phrase"] += [word["word"]]
    state["duration"] += word_time

def clear_state(state):
    state["phrase"] = []
    state["duration"] = 0.0

def add_phrase(state, output):
    phrase =  " ".join(state["phrase"])
    if phrase.isspace() or phrase == "":
        phrase = "..."
        
    output.append({
        "phrase": phrase,
        "duration": state["duration"],
        "wait": 0
    })
    clear_state(state)

def flatten_segment(result):
    words = []
    for seg in result["segments"]:
        words.extend(seg["words"])
    return words

def fill_gaps(words):
    if words[0]["start"] != 0:
        words = [{
            "word": "",
            "start": 0.0,
            "end": words[0]["start"],
            "probability": 1.0
        }] + words
    for i in range(len(words)-1):
        gap = words[i+1]["start"] - words[i]["end"]
        if (gap > 0):
            words.append({
                "word": "",
                "start": words[i]["end"],
                "end": words[i+1]["start"],
                "probability": 1.0
            })
    def sort_by_start(e):
        return e["start"]
    words.sort(key=sort_by_start)
    return words
            

def subtitle(change_every, result):
    """Create a subtitle structure from a whisper transcription.

    Args:
    	change_every: approximate number of seconds between subtitle switches
    	result: the output of whisper.transcribe(..., word_timestamps=True)
    Returns:
    	A list of dictionaries with keys (phrase, duration, wait) giving the
    	phrase to display, the duration to show it, and how long to wait to show
    	it from the previous subtitle.
    """

    words = flatten_segment(result)
    words = fill_gaps(words)
    output = []
    state = {}
    clear_state(state)
    for word in words:
        add_word(state, word)
        if state["duration"] > change_every:
            add_phrase(state, output)
    return output

def format_mpsub(subtitles, title):
    """Writes out subtitles in mpsub format.

    Args:
    	subtitles: the output of make_st.subtitle
    	title: the title of the video
    Returns:
    	A string containing the subtitles in mpsub format.
    """

    out = "\n".join([
        f"TITLE={title}",
        "TYPE=VIDEO",
        "FORMAT=TIME"
    ]) + "\n\n"
    for phrase in subtitles:
        out += f"{phrase['wait']} {phrase['duration']}\n"
        out += phrase["phrase"]
        out += "\n\n"
    return out

def create_subtitles_from_video(video_path, video_title, model_name, change_every):
    model = whisper.load_model(model_name)
    result = whisper.transcribe(model, video_path, word_timestamps=True)
    st = subtitle(change_every, result)
    return format_mpsub(st, video_title)

if __name__=="__main__":
    fn = sys.argv[1]
    title = sys.argv[2]
    if len(sys.argv) > 3:
        change_every = float(sys.argv[3])
    else:
        change_every = 5.0
    
    if len(sys.argv) > 4:
        model_name = sys.argv[4]
    else:
        model_name = "base"


    print(create_subtitles_from_video(fn, title, model_name, change_every))


