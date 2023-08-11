import os
from png_process import parse_parameters

main_keys = ['test', 'parameters', 'Negative prompt', 'Steps', 'Lora hashes']


# 参数大致分割为以上四部分或三部分
def spilt_general(params, keys):
    result = []
    temp = []
    for v in keys:
        parts = [part.strip() for part in filter(None, params.partition(v))]
        print(len(parts))
        if len(parts) <= 1:
            continue
        if parts[1].startswith(':'):
            parts[1] = parts[1].lstrip(':')
        parts[0] = parts[0] + ':\\n'
        temp.append(''.join(parts))
    return ''.join(result)

# 参数详细分割为字典
def spilt_details(params):
    pass


# 完整参数输出到临时文件
def write_to_temp(name, params):
    with open(f'out/temp/t{name}.txt', 'w', encoding='utf-8') as f:
        f.write(params)


# 参数大致分割后输出到临时文件
def write_to_general(name, params):
    with open(f'out/temp_general/g{name}.txt', 'w', encoding='utf-8') as f:
        f.write(params)


# 参数详细分割后输出到临时文件
def write_to_detailed(name, params):
    with open(f'out/temp_detailed/d{name}.txt', 'w', encoding='utf-8') as f:
        f.write(params)


# 从完整参数的临时文件中读取参数信息
def read_to_temp(name):
    with open(f'out/temp/t{name}.txt', 'r', encoding='utf-8') as f:
        return f.read()


# 从大致分割的临时文件中读取参数信息
def read_to_general(name):
    with open(f'out/temp_general/g{name}.txt', 'r', encoding='utf-8') as f:
        return f.read()


# 从详细分割的临时文件中读取参数信息
def read_to_detailed(name):
    with open(f'out/temp_detailed/d{name}.txt', 'r', encoding='utf-8') as f:
        return f.read()


# 图片地址
input_path = 'img/pp/1.png'

# 图片名称
input_name = os.path.basename(input_path).split('.')[0]

# 解析出所有参数
# all_params = parse_parameters(input_path)

# 写入完整参数的临时文件
# write_to_temp(input_name, all_params)

# 从完整参数的临时文件读取
all_params = read_to_temp(input_name)

# 参数大致分割
general_params = spilt_general(all_params, main_keys)
write_to_general(input_name, general_params)
# print(general_params)
