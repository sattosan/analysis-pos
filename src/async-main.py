import asyncio
import collections
import time

import spacy

import config


nlp = spacy.load('ja_ginza')
pos_counter = collections.Counter()


# 品詞の出現回数をカウント
def count_pos_of_token(keyword):
    # 形態素解析
    nlp_keyword = nlp(keyword)
    for sent in nlp_keyword.sents:
        for token in sent:
            pos_counter[token.pos_] += 1


async def main():
    tasks = []
    with open(config.INPUT_FILEPATH, mode="r") as f:
        for keyword in f:
            # 形態素解析は処理が重いのでブロッキングしないようスレッド化
            tasks.append(asyncio.to_thread(count_pos_of_token, keyword))
    # 並列実行
    await asyncio.gather(*tasks, return_exceptions=True)
    print(pos_counter)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f"time: {time.time() - start}")
