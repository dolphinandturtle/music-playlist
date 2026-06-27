import json
import itertools


with open("music.json", "r") as file:
    music = json.load(file)

for i, j in itertools.combinations(range(len(music)), 2):
    if "source" in music[i] and "source" in music[j]:
        if music[i]["source"] == music[j]["source"]:
            print("Clashing files", music[i], music[j])
            exit()

images = set()
calls = []
for song in music:
    if "source" not in song:
        print(f"# Missing song... {song['title']}")
        continue
    filename = song["source"]
    if filename.count('.') == 0:
        continue
    *rest, ext = filename.split('.')
    filetitle = '.'.join(rest)
    metadata = []
    if "title" in song:
        #metadata.append("-metadata " + "title" + '=' + '"' + song["title"].replace("\"", "\\\"").replace("$", "\\$") + '"')
        title = song["title"].replace("\"", "\\\"").replace("$", "\\$")
        metadata.append(f"--title \"{title}\"")
    if "author" in song:
        if isinstance(song["author"], str):
            author = song["author"]
        elif isinstance(song["author"], list):
            author = ', '.join(song["author"])
        else:
            raise Exception
        author = author.replace("\"", "\\\"").replace("$", "\\$")
        metadata.append(f"--artist \"{author}\"")
        #metadata.append("-metadata " + "artist" + '=' + '"' + author.replace("\"", "\\\"").replace("$", "\\$") + '"')
    if "album" in song:
        album = song["album"].replace("\"", "\\\"").replace("$", "\\$")
        metadata.append(f"--album \"{album}\"")
        #metadata.append("-metadata " + "album" + '=' + '"' + song["album"].replace("\"", "\\\"").replace("$", "\\$") + '"')
    if "date" in song:
        metadata.append(f"--date \"{song['date']}\"")
        #metadata.append("-metadata " + "date" + '=' + '"' + song["date"].replace("\"", "\\\"").replace("$", "\\$") + '"')
    if "queue" in song:
        metadata.append(f"--tracknumber \"{song['queue']}\"")
    if "cover" in song:
        images.add(song['cover'])
        *_rest, _ext = song['cover'].split('.')
        _title = '.'.join(_rest)
        image_jpg = f"uimage/{_title.split('/')[-1]}.jpg"
        metadata.append(f"--picture \"{image_jpg}\"")
        #metadata.append("-metadata " + "track" + '=' + '"' + str(song["queue"]).replace("\"", "\\\"").replace("$", "\\$") + '"')
    metadata = ' '.join(metadata)
    #calls.append(f"ffmpeg -i {song['source']} -map_metadata -1 -c copy {metadata} -c:a libopus -b:a 64k umusic/{filetitle.split('/')[-1]}.opus")
    calls.append(f"(ffmpeg -i {song['source']} -map_metadata -1 -map a umusic/{filetitle.split('/')[-1]}.flac && opusenc --quiet --bitrate 64k {metadata} umusic/{filetitle.split('/')[-1]}.flac umusic/{filetitle.split('/')[-1]}.opus && rm umusic/{filetitle.split('/')[-1]}.flac)")

calls_images = []
for img in images:
    *rest, ext = img.split('.')
    title = '.'.join(rest)
    calls_images.append(f"(ffmpeg -i {img} -vf scale=300:-1 uimage/{title.split('/')[-1]}.jpg)")

print(' | '.join(calls_images))
print(' | '.join(calls))
