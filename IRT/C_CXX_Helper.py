import re

C_VAR_NAME = re.compile('[_a-zA-Z]+[_a-zA-Z0-9.\\[\\]]*')

C_CPP_KEYWORDS = {'auto', 'break', 'case', 'catch', 'char', 'const',
                  'continue', 'default', 'do', 'double', 'else',
                  'enum', 'extern', 'float', 'for', 'goto', 'if',
                  'int', 'long', 'register', 'return', 'short',
                  'signed', 'sizeof', 'static', 'struct', 'switch', 'try',
                  'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', 'when'}

def are_all_letters_uppercase(s:str):
    letters = [char for char in s if char.isalpha()]
    return all(letter.isupper() for letter in letters)

def name_filter(lstr: str, it: iter, cap_assert:bool) -> list[str]:
    """
    用简易快速的办法过滤不可能是变量名的字符串
    1. 变量名周围不应有引号
    2. 变量名周围括号的存在应该合法
    3. 假设全大写字母名称为常量或者宏
    4. 排除C/C++关键字
    :param cap_assert: 假设全大写字母名称为常量或者宏
    :param lstr: 包含该字符串的代码行
    :param it: re.match 类型的 iter
    :return: 过滤后的字符串 list
    """
    res = []
    for name in it:
        start = name.start()
        end = name.end()
        if (lstr[max(0, start - 1)] == '\'' or lstr[max(0, start - 1)] == '\"'
                or lstr[min(len(lstr) - 1, end)] == '\'' or lstr[min(len(lstr) - 1, end)] == '\"'
                or lstr[max(0, start - 1)] == ')' or lstr[min(len(lstr) - 1, end)] == '(' ):
            continue
        if (lstr[start:end] not in res and lstr[start:end] not in C_CPP_KEYWORDS
                and (not are_all_letters_uppercase(lstr[start:end]) or not cap_assert)):
            res.append(lstr[start:end])
    return res