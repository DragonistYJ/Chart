def read_data(file_path, channels):
    """
    从文件中读取波形数据，并返回
    :param file_path: 文件路径
    :param channels: 通道数量
    :return: 每一个通道的信号，形状为[channels, size]
    """
    result = []
    for i in range(channels):
        result.append([])
    try:
        with open(file_path, mode='rb') as f:
            data = f.read()

            for i in range(0, len(data), 2):
                channel = i // 2 % channels
                number = int.from_bytes(data[i:i + 2], byteorder="big", signed=True)
                result[channel].append(number)
    except FileNotFoundError:
        print(file_path, "not exist")
        return result
    return result
