import unicodedata


# 判断字符串是否是可打印字符
def is_printable(s):
    return all(unicodedata.category(c) not in ('Cc', 'Cf') for c in s)


# 解码字符串，直到遇到无法解码的字符
def decode_until_invalid_utf8(data):
    try:
        return data.decode('utf-8'), True
    except UnicodeDecodeError as e:
        return data[:e.start].decode('utf-8'), False
