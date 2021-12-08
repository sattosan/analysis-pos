import collections
import time

import spacy
from tqdm import tqdm

import config
import utils


# 日本語辞書の読み込み
nlp = spacy.load('ja_ginza')
# 品詞カウント用
pos_counter = collections.Counter()


# 品詞の出現回数をカウント
def count_pos_of_token(keyword):
    try:
        token_pos_pair = ''
        # 形態素解析
        nlp_keyword = nlp(keyword)
        for sent in nlp_keyword.sents:
            for token in sent:
                token_pos_pair += f'{token.text}:{token.pos_}|'
                pos_counter[token.pos_] += 1
        return {'keyword': keyword, 'token_pos': token_pos_pair}
    except Exception:
        return {'keyword': keyword, 'token_pos': 'None'}


def main():
    # ファイル読み込み
    keywords = utils.get_file_contents(config.INPUT_FILEPATH, limit=None)

    print('========形態素解析開始========')
    result_csv = []
    for keyword in tqdm(keywords, total=len(keywords)):
        result_csv.append(count_pos_of_token(keyword))
    print('========形態素解析完了========')

    # ファイル書き込み
    utils.write_contents(config.NORMAL_OUTPUT_DIRPATH, result_csv)

    jp_pos_counter = utils.to_jp_keys_of_pos_counter(pos_counter)
    print(jp_pos_counter)
    # 品詞数を棒グラフ化した画像を生成
    utils.generate_graph(config.NORMAL_OUTPUT_DIRPATH, jp_pos_counter)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"実行時間: {end - start}s")
