from .constants import (
    PUNCTUATION,
    WORD_DOCUMENT_JOIN_STRING,
)


def tokenize_content(content):
    """
        We inherit the rules from the App Engine Search API
        when it comes to punctuation.

        We have a list of punctuation chars which break the
        content into tokens, and then some special cases where it
        makes sense. You can find the rules documented here:
        https://cloud.google.com/appengine/docs/standard/python/search#special-treatment
    """

    tokens = []
    current = ""

    STOP_CHARS = list(PUNCTUATION) + [" "]

    for c in content:
        if c in STOP_CHARS:
            if current.strip():
                tokens.append(current)

            if c.strip() and c != WORD_DOCUMENT_JOIN_STRING:
                tokens.append(c)

            current = ""
        else:
            current += c
    else:
        if current.strip():
            tokens.append(current)

    new_tokens = []
    tokens_to_append = []
    indexes_to_remove = []

    ACRONYM_TOKENS = (".", "-")
    current_at = None

    # Detect acronyms
    acronym_run = 0
    for i, token in enumerate(tokens):
        if (
            ((acronym_run and token == current_at) or (not acronym_run and token in ACRONYM_TOKENS)) and
                i > 0 and tokens[i - 1] != token
        ):
            acronym_run += 1
            if acronym_run == 1:
                current_at = token
        else:
            if acronym_run > 1 and token != current_at:
                start = i - (2 * acronym_run)

                original = "".join(tokens[start:start + (acronym_run * 2) + 1])
                parts = [tokens[start + (x * 2)] for x in range(acronym_run + 1)]
                acronym = "".join(parts)

                # Add variations of the acronym
                new_tokens.append(acronym)
                new_tokens.append(".".join(parts))
                new_tokens.append("-".join(parts))

                # Remove the original characters
                indexes_to_remove.extend(range(start, start + (acronym_run * 2) + 1))

                if original in new_tokens:
                    new_tokens.remove(original)

                # Extend a single token made up of the whole original acronym
                # rather than seperate chars
                tokens_to_append.append(original)

                acronym_run = 0
            elif i > 0 and tokens[i - 1] != current_at:
                acronym_run = 0

    tokens = [x for i, x in enumerate(tokens) if i not in indexes_to_remove]
    tokens.extend(tokens_to_append)
    return tokens, new_tokens
