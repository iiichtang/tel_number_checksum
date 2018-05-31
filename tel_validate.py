from country_call_code import *
from area_code import *
#from tel_list_for_test import *

CELL_PHONE_DICT = {'13': 1, '14': 1, '15': 1, '17': 1, '18': 1}
HOTLINE_FIVE_DIGIT_DICT = {'10': 1, '11': 1, '12': 1}
HOTLINE_TEN_DIGIT_DICT = {'400': 1, '800': 1}
TELECOM_DICT = {'10010': 1, '10000': 1, '10001': 1, '10086': 1}


def tel_validate(tel_string):
    """
    Telephone number validation
    :param tel_string: tel number
    :return: Validate result of tel number
    """
    if len(tel_string) < 3:
        return False

    # Cell phone
    if tel_string[0:2] in CELL_PHONE_DICT and len(tel_string) == 11:
        # print("cell phone")
        return True

    # 10, 11, 12 Hotline
    if tel_string[0:2] in HOTLINE_FIVE_DIGIT_DICT and len(tel_string) == 5:
        # print("95, 12 Hotline")
        return True

    # 95, 095 Long tel
    if (tel_string.startswith("95") or tel_string.startswith("095")) and 5 <= len(tel_string) <= 17:
        # print("SMS")
        return True

    # 400, 800 Hotline
    if tel_string[0:3] in HOTLINE_TEN_DIGIT_DICT and len(tel_string) == 10:
        # print("400, 800 Hotline")
        return True

    # Telecom
    if tel_string[0:5] in TELECOM_DICT and len(tel_string) <= 15:
        # print("telecom")
        return True

    # 1010 Hotline
    if tel_string.startswith("1010") and len(tel_string) == 8:
        # print("1010 Hotline")
        return True

    # SMS
    if tel_string.startswith("106") or tel_string.startswith("125"):
        # print("SMS")
        return True

    # Special hotline
    if tel_string.startswith("1") and len(tel_string) == 3:
        # print("Special hotline")
        return True

    # Remove area code
    tel_without_area_code = remove_area_code(tel_string)
    if tel_without_area_code is not False:
        # 96 Hotline
        if tel_without_area_code.startswith("96") and 5 <= len(tel_without_area_code) <= 7:
            # print("96 Hotline")
            return True

        # 10, 11, 12 Hotline
        if tel_without_area_code[0:2] in HOTLINE_FIVE_DIGIT_DICT and len(tel_without_area_code) == 5:
            # print("95, 12 Hotline")
            return True

        # 95 Long tel
        if tel_without_area_code.startswith("95") and 5 <= len(tel_without_area_code) <= 17:
            # print("SMS")
            return True

        # Telecom
        if tel_without_area_code[0:5] in TELECOM_DICT and len(tel_without_area_code) <= 15:
            # print("telecom")
            return True

        # Normal tel
        if 7 <= len(tel_without_area_code) <= 8:
            # print("Normal tel")
            return True
    return False


def remove_area_code(tel_string):
    """
    Remove local area digits from a telephone number
    :param tel_string: Tel number
    :return: Tel number without local area digits
    """
    area_code_length = 0
    if tel_string[:4] in AREA_FOUR_DIGIT_DICT:
        area_code_length = 4
    elif tel_string[:3] in AREA_THREE_DIGIT_DICT:
        area_code_length = 3

    if area_code_length > 0:
        # print(tel_string[area_code_length:])
        return tel_string[area_code_length:]
    return False


def region_check(tel_string):
    """
    Telephone number validation with global region digits
    :param tel_string: Tel number
    :return: Validate result of tel number
    """
    # Check if + exist in the first digit
    if not tel_string.startswith("+") and not tel_string.startswith("00"):
        return False

    # Remove Leading Symbol
    tel_no_leading_symbol = ""
    if tel_string.startswith("+"):
        tel_no_leading_symbol = tel_string[1:]
    elif tel_string.startswith("00"):
        tel_no_leading_symbol = tel_string[2:]

    # Check if tel number contain any non int charactor
    if not str(tel_no_leading_symbol).isdigit():
        return False

    # In America
    if tel_no_leading_symbol.startswith("1"):
        # print("+1 region")
        return True

    # In China
    if tel_no_leading_symbol.startswith("86"):
        local_tel_without_region = tel_no_leading_symbol[2:]
        tel_first_three = local_tel_without_region[:3]
        tel_first_two = local_tel_without_region[:2]
        if tel_first_three in AREA_FOUR_DIGIT_WITHOUT_ZERO_DICT or tel_first_two in AREA_THREE_DIGIT_WITHOUT_ZERO_DICT:
            local_tel = "0" + local_tel_without_region
        else:
            local_tel = local_tel_without_region

        if tel_validate(local_tel):
            # print("+86 region")
            return True
        return False

    # In other country
    tel_first_three = tel_no_leading_symbol[:3]
    tel_first_two = tel_no_leading_symbol[:2]

    if tel_first_three in COUNTRY_CODE_DICT or tel_first_two in COUNTRY_CODE_DICT:
        # print("+xx region")
        return True

    return False


def tel_reform(tel_number):
    """
    Check and reform the telephone number
    :param tel_number: Tel number
    :return: Reformed tel number. Return None if the tel is not valid
    """
    tel_string = str(tel_number).replace("-", "")

    # Region check
    if tel_string.startswith("+") or tel_string.startswith("00"):
        if region_check(tel_string):
            return tel_string
        return None

    # Digit check
    if not tel_string.isdigit():
        return None

    # Validate check
    if tel_validate(tel_string):
        return tel_string

    return None


if __name__ == "__main__":
    """
    for tel in valid_86_region_list:
        result = tel_reform(tel)
        if result is None:
            print("%s => False" % tel)
        else:
            print("%s => %s" % (tel, tel_reform(tel)))
    """
    print(tel_reform("10010"))
    print(tel_reform("01010010"))