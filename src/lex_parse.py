from language_spec import *


def lex_parse(expr: str):
    expr = expr.lower()
    tokens = []
    idx = 0
    while (idx < len(expr)):
        current_slice = expr[idx:]

        matches = [regex.search(current_slice) for regex in token_res]

        new_token = None
        # dummy string has len 1 so idx will advance by 1 char each iter if none found
        match_str: str = " "
        # the order of these is important, in cases of multiple matches first one takes precedence

        for match, type_ in zip(matches, token_res.values()):
            if (match is not None and match.start() == 0):
                match_str = str(match.group(0))

                new_token = Token(name=match_str, type_=type_)
                break
        idx += len(match_str)
        if (new_token is not None):
            tokens.append(new_token)
    return tokens
