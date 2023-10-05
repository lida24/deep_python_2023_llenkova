from typing import Generator


def process_line(line, search_words, found_lines) -> Generator[str, None, None]:
    words = line.strip().lower().split()
    for phrase in search_words:
        phrase_words = phrase.strip().lower().split()
        if all(word in words for word in phrase_words):
            if line not in found_lines:
                found_lines.add(line)
                yield line.rstrip("\n").strip()


def search_phrases(file, search_words) -> Generator[str, None, None]:
    found_lines = set()
    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_object:
            for line in file_object:
                yield from process_line(line, search_words, found_lines)
    else:
        for line in file:
            yield from process_line(line, search_words, found_lines)


def process_file(file, search_words) -> list[str]:
    return list(search_phrases(file, search_words))
