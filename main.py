import data_models

def main():
    txt_source = "./hurdat_sample.txt"
    m = data_models.TextSource(source_path=txt_source)
    ds =m.extract_data()
    for track in ds.tracks:
        print(track.year + track.cyclone_no)
        for track_entry in track.track_entries:
            print(track_entry)

if __name__ == "__main__":
    main()