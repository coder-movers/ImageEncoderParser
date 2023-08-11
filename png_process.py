import struct
import re
from png_tool import is_printable, decode_until_invalid_utf8


# 解析PNG文件数据
def parse_parameters(input_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    i = 8  # 跳过PNG文件的签名

    chunks_data = b''
    while i < len(data):
        length = struct.unpack('>I', data[i:i + 4])[0]  # 读取块长度
        chunk_data = data[i + 8:i + 8 + length]  # 读取块数据

        chunks_data += chunk_data
        i += length + 12

    parameters_bytes = b'parameters'
    start_index = chunks_data.find(parameters_bytes)

    # 判断是否有parameters
    if start_index == -1:
        return

    # 在第一个无法被utf-8识别的字符停止
    decoded_chunk, _ = decode_until_invalid_utf8(chunks_data[start_index:])

    # 检查 decoded_chunk 的最后一个字符，如果它不是可打印的，就从 decoded_chunk 中移除
    if decoded_chunk[-1] != is_printable(decoded_chunk[-1]):
        decoded_chunk = decoded_chunk[:-1]

    # 将不可被打印字符替换成空格
    cleaned_text = ''.join(c if is_printable(c) else ' ' for c in decoded_chunk)

    # 连续多个空格合并成一个空格
    cleaned_text = re.sub(' +', ' ', cleaned_text)

    return cleaned_text


def remove_parameters(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    i = 8

    new_data = bytearray(data[:i])  # 将文件的前8个字节（PNG签名）添加到新数据中

    while i < len(data):
        length = struct.unpack('>I', data[i:i + 4])[0]
        chunk_type = data[i + 4:i + 8]
        chunk_data = data[i + 8:i + 8 + length]
        crc = data[i + 8 + length:i + 12 + length]

        if chunk_type == b'tEXt':
            parameters_bytes = b'parameters'
            if chunk_data.find(parameters_bytes) == -1:
                # 如果数据块不包含参数信息，则将其添加到新数据中
                new_data.extend(data[i:i + 12 + length])
        else:
            # 将其他类型的数据块添加到新数据中
            new_data.extend(data[i:i + 12 + length])

        i += length + 12

    with open(output_path, 'wb') as f:
        f.write(new_data)
