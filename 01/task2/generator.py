from typing import Generator


def search_phrases(file, search_words) -> list:
    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_object:
            return list(process_file(file_object, search_words))
    else:
        return list(process_file(file, search_words))


def process_file(file, search_words) -> Generator[str, None, None]:
    for line in file:
        for word in search_words:
            if word.lower() in line.strip().lower().split(" "):
                yield line.rstrip("\n").strip()
