from reading import count_mentions, greet, size_label, total_kilometres, word_count


def test_greet_puts_the_name_in_the_greeting():
    assert greet("Mia") == "G'day, Mia!"


def test_word_count_counts_words():
    assert word_count("Ironbark Line Freight runs trucks") == 5


def test_word_count_of_empty_text_is_zero():
    assert word_count("") == 0


def test_size_label_short():
    assert size_label(99) == "short"


def test_size_label_medium_includes_both_ends():
    assert size_label(100) == "medium"
    assert size_label(500) == "medium"


def test_size_label_long():
    assert size_label(501) == "long"


def test_total_kilometres_adds_every_trip():
    assert total_kilometres([120, 85, 400]) == 605


def test_total_kilometres_of_no_trips_is_zero():
    assert total_kilometres([]) == 0


def test_count_mentions_ignores_case():
    words = ["Ironbark", "hauls", "freight", "IRONBARK", "ironbark", "trucks"]
    assert count_mentions(words, "ironbark") == 3


def test_count_mentions_when_missing():
    assert count_mentions(["trucks", "depots"], "ironbark") == 0
