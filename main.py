import logging

import repositories
import domain_models


def main():
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)

    txt_source = "./Tests/Test_Data/hurdat_sample.txt"
    m = repositories.TextRepository(source_path=txt_source)
    ds = m.extract_data()
    for track in ds:
        print(track.year + track.cyclone_no)
        for track_entry in track.track_entries:
            print(track_entry)

if __name__ == "__main__":
    main()