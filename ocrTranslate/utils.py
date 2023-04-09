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


def format_words(words_list):
    """
    Formatuje listę słów i zwraca je w postaci ciągu znaków z oddzieleniem przez nową linię.
    Jeśli argumentem jest ciąg znaków, to zwraca ten ciąg bez żadnych zmian.
    """
    formatted_words = ""
    if isinstance(words_list, str):
        formatted_words = words_list
    elif isinstance(words_list, list):
        for word in words_list:
            if word.strip():  # sprawdza, czy słowo nie jest puste ani nie składa się tylko ze znaków białych
                formatted_words += word.strip() + "\n"
    return formatted_words.strip()


def format_words2(word):
    words = ""
    if type(word) != str:
        for i in word:
            if i != "":
                words = words + i + "\n"
    else:
        words = word
    return words