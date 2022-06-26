from FLP import FLPFile

if __name__ == "__main__":
    x = FLPFile("tests/untitled.flp")
    x.parse()
    for idx, track in enumerate(x):
        track.parse()
        print(track)

# keep it simple = v 11.5.14
# NewStuff = v 10.0.0
