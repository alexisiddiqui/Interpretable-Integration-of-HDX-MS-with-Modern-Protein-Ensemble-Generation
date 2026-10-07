"""Page labels are strings; PDF indices are one-based and never inferred by a viewer."""


def roman(number):
    result = ""
    for value, label in (
        (1000, "m"),
        (900, "cm"),
        (500, "d"),
        (400, "cd"),
        (100, "c"),
        (90, "xc"),
        (50, "l"),
        (40, "xl"),
        (10, "x"),
        (9, "ix"),
        (5, "v"),
        (4, "iv"),
        (1, "i"),
    ):
        count, number = divmod(number, value)
        result += label * count
    return result


def page_index(document):
    return {
        p["label"]: p["pdf_index"]
        for p in document["pagemap"]["pages"]
        if p["label"] is not None
    }
