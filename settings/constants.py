import re

class GlobalConstants:

    ## 7-16 chars with digits, no special characters.
    USERNAME_REGEX = re.compile(r'^[a-zA-z0-9]{7,16}')
    USERNAME_REGEX_STR = '^[a-zA-z0-9]{7,16}'

    # 'john.doe@email.com'
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    EMAIL_REGEX_STR = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # 1 UC char, 1 LC char, 1 NUM char; between 8 to 15 chars
    PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    PASSWORD_REGEX_STR = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    REGNAL_NUMBERS = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
        7: "VII",
        8: "VIII",
        9: "IX",
        10: "X",
        11: "XI",
        12: "XII",
        13: "XIII",
        14: "XIV",
        15: "XV",
        16: "XVI",
        17: "XVII",
        18: "XVIII",
        19: "XIX",
        20: "XX",
        21: "XXI",
        22: "XXII",
        23: "XXIII",
        24: "XXIV",
        25: "XXV"
    }