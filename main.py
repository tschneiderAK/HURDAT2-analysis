import data_models

def main():
    txt_source = "./hurdat_sample.txt"
    m = data_models.TextSource(source_path=txt_source)
    print(m.extract_data())

if __name__ == "__main__":
    main()