import re


REQUIRED_SECTIONS = [
    "education",
    "experience",
    "skills",
    "projects",
    "contact"
]


ACTION_VERBS = [
    "developed",
    "created",
    "implemented",
    "designed",
    "managed",
    "built",
    "improved",
    "analyzed",
    "led",
    "optimized",
    "tested",
    "created",
    "maintained",
    "configured",
    "integrated",
    "automated"
]


def calculate_ats_score(text):

    text_lower = text.lower()

    score = 0

    details = {}


    # -------------------------
    # SECTION CHECK
    # -------------------------

    found_sections = []

    for section in REQUIRED_SECTIONS:

        if section in text_lower:
            found_sections.append(section)


    section_score = min(
        int(
            (len(found_sections) /
             len(REQUIRED_SECTIONS)) * 25
        ),
        25
    )

    score += section_score


    details["sections"] = {
        "found": found_sections,
        "missing": [
            section
            for section in REQUIRED_SECTIONS
            if section not in found_sections
        ],
        "score": section_score
    }


    # -------------------------
    # WORD COUNT
    # -------------------------

    words = text.split()

    word_count = len(words)


    if 300 <= word_count <= 1000:

        length_score = 20

    elif 150 <= word_count < 300:

        length_score = 12

    elif word_count > 1000:

        length_score = 15

    else:

        length_score = 5


    score += length_score

    details["word_count"] = word_count

    details["length_score"] = length_score


    # -------------------------
    # ACTION VERBS
    # -------------------------

    found_verbs = []

    for verb in ACTION_VERBS:

        if re.search(
            r"\b" + re.escape(verb) + r"\b",
            text_lower
        ):

            found_verbs.append(verb)


    action_score = min(
        len(found_verbs) * 2,
        20
    )


    score += action_score

    details["action_verbs"] = found_verbs

    details["action_score"] = action_score


    # -------------------------
    # CONTACT
    # -------------------------

    email_found = bool(
        re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            text
        )
    )


    phone_found = bool(
        re.search(
            r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
            text
        )
    )


    contact_score = 10


    if not email_found:
        contact_score -= 5


    if not phone_found:
        contact_score -= 5


    score += contact_score


    details["contact"] = {
        "email": email_found,
        "phone": phone_found,
        "score": contact_score
    }


    # -------------------------
    # BASIC COMPLETENESS
    # -------------------------

    formatting_score = 15


    if word_count < 100:
        formatting_score = 5

    elif word_count < 150:
        formatting_score = 10


    score += formatting_score


    details["completeness_score"] = formatting_score


    # -------------------------
    # FINAL SCORE
    # -------------------------

    score = max(
        0,
        min(score, 100)
    )


    return score, details