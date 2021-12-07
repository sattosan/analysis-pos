import concurrent.futures
import collections
import threading
import time

import spacy
from tqdm import tqdm

import config
import utils


# 日本語辞書の読み込み
nlp = spacy.load('ja_ginza')
# スレッドで変数を共有するためのロックを使う
lock = threading.Lock()
# 品詞カウント用
pos_counter = collections.Counter()


# 品詞の出現回数をカウント
def count_pos_of_token(keyword):
    try:
        # スレッド間で共通の変数を使うのでエラーにならないようにロックする
        with lock:
            # 形態素解析
            nlp_keyword = nlp(keyword)
            token_pos_pair = ""
            for sent in nlp_keyword.sents:
                for token in sent:
                    token_pos_pair += f"{token.text}:{token.pos_}|"
                    pos_counter[token.pos_] += 1
            return {'keyword': keyword, 'token_pos': token_pos_pair}
    except Exception:
        return {'keyword': keyword, 'token_pos': 'None'}


def main():
    # ファイル読み込み
    keywords = utils.get_file_contents(config.INPUT_FILEPATH, limit=None)

    # 複数スレッドを使って並列実行
    print('========形態素解析開始========')
    result_csv = []
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        for keyword in keywords:
            tasks.append(executor.submit(count_pos_of_token, keyword))
        # 処理が終わったタスクは随時プログレスバーに反映される
        for future in tqdm(concurrent.futures.as_completed(tasks), total=len(tasks)):
            try:
                # 処理が終わらないとき用にタイムアウトを設定
                result = future.result(timeout=config.THREAD_TIMEOUT)
                # 結果をつめる
                result_csv.append(result)
            except concurrent.futures.TimeoutError:
                print("this took too long...")
    print(pos_counter)
    print('========形態素解析完了========')

    # ファイル書き込み
    utils.write_contents(config.THREAD_OUTPUT_DIRPATH, result_csv)

    jp_pos_counter = utils.to_jp_keys_of_pos_counter(pos_counter)
    print(jp_pos_counter)
    # 品詞数を棒グラフ化した画像を生成
    utils.generate_graph(config.THREAD_OUTPUT_DIRPATH, jp_pos_counter)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"実行時間: {end - start}s")
