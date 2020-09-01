import random
class Random_func:
    #idをランダムに生成するメソッド
    def random_id_hexadecimal():
        source_str = 'ABCDEF1234567890'
        random.choice(source_str)
        return "".join([random.choice(source_str) for x in range(32)])

