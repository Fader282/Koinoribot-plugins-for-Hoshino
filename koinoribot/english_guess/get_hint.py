import json
import os.path


def get_hint(
        in_word: str,  # 在单词里，但位置不对
        incorrect: str,
        length: int,
        correct: dict = None,  # 位置正确的字母
):
    in_word = list(in_word)
    incorrect = list(incorrect)
    possible_words = []
    legal_words = json.load(open(os.path.join(os.path.dirname(__file__), 'data/check_list.json')))
    target_words = legal_words[length]
    for word in target_words:
        # print(word)
        count = 0
        for alphabet in word:
            if alphabet in incorrect:
                count += 1
        if not count:
            possible_words.append(word)
            continue
        else:
            count = 0

    advance = []  # 进一步
    for word in possible_words:
        count = 0
        for alphabet in in_word:
            if alphabet in word:
                count += 1
        if count == len(in_word):
            advance.append(word)
            count = 0


    if correct:
        exact = []
        for word in advance:
            word = list(word)
            count = 0
            for k, v in correct.items():
                if word[v] == k:
                    count += 1
            if count == len(list(correct.keys())):
                exact.append(word)
        return exact
    else:
        return advance

if __name__ == '__main__':
    a = get_hint(
        'sel',  # 这些字母在单词里
        'banktxporu',  # 这些字母不在单词里
        7)  # 单词长度
    print(a)  # 输出所有可能的单词
