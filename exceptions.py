import re


def process_compare(compare, image):
    if "type" not in compare:
        print("Compare data deos not have any type property")
        return False

    if "compare" not in compare:
        print("Compare data deos not have any compare property")
        return False

    flip = False

    if "flip" in compare:
        flip = bool(compare["flip"])

    result = False

    if compare["type"] == "regex":
        p = re.compile(compare["compare"])
        result = p.match(image) != None
    elif compare["type"] == "equals":
        result = image in compare["compare"]
    else:
        print("Compare data does not have any criteria property")

    if flip:
        return not result
    else:
        return result


def process_criteria(criteria, metadata):
    if "trait" in criteria and criteria["trait"] not in metadata:
        return False

    return process_compare(criteria, metadata[criteria["trait"]])


def should_exclude_image(exceptions, metadata, layer, image):
    for exception in exceptions:
        if "type" not in exception:
            print("Exception does not have any type property")
            continue

        if "criteria" not in exception:
            print("Exception does not have any criteria property")
            continue

        if "data" not in exception:
            print("Exception does not have any data property")
            continue

        if exception["type"] == "remove":
            if "trait" in exception["data"] and layer != exception["data"]["trait"]:
                continue

            shouldBeRemoved = process_compare(exception["data"], image)

            if not shouldBeRemoved:
                continue

            if not process_criteria(exception["criteria"], metadata):
                continue

            return True
        else:
            print(f"Unknown exception type: {exception['type']}")

    return False
