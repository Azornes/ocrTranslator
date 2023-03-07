def list_to_string(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele + " "
    return str1


def parse_html_link(link):
    if '//' in link:
        link = link.replace('//', '\\')
    elif '/' in link:
        link = link.replace('/', '\\')
    if '\\' in link:
        pass
    elif "\\\\" in link:
        link = link.replace('\\\\', '\\')
    return link


def print_error_msg(msg, where):
    print("\n\033[91m" + "Error name: " + str(msg) + "\nException occurs in: " + str(where) + "\033[0m")