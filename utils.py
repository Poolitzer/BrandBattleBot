import re


def get_brands(string):
    temp = re.findall(r"(?i)([\w ]+)( vs\. | vs )([\w ]+)", string)
    if temp:
        return [temp[0][0], temp[0][2]]
    else:
        return False


def get_percentages(num1, num2):
    percent_1 = num1 / (num1 + num2) * 100
    percent_2 = num2 / (num1 + num2) * 100
    return ['{0:.0f}%'.format(percent_1), '{0:.0f}%'.format(percent_2)]
