import random

proverbs = [
    {"text": "बिल्ली के गले में घंटी कौन बाँधेगा?", "likes": 997, "views": 309},
    {"text": "ऊँट के मुँह में जीरा", "likes": 452, "views": 231},
    {"text": "घर का भेदी लंका ढाए", "likes": 785, "views": 402},
]

def get_random_proverb():
    return random.choice(proverbs)
