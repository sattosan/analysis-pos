import csv
import datetime

import emoji
import japanize_matplotlib
import neologdn
import matplotlib.pyplot as plt
import mojimoji
import re
from tqdm import tqdm

import config


def preprocessing(text):
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\r', '', text)
    text = re.sub(r'\s', '', text)
    text = text.lower()
    text = mojimoji.zen_to_han(text, kana=True)
    text = mojimoji.han_to_zen(text, digit=True, ascii=True)
    text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
    text = neologdn.normalize(text)

    return text


def checkAlnum(text):
    alnum = re.compile(r"^[a-zA-ZＡ-Ｚ0-9-.ー+ ™']+$")
    result = alnum.match(text) is not None
    return result


def get_file_contents(input_filepath, limit=None):
    print('========ファイル読み込み開始========')
    contents = []
    # プログレスバー表示のため予めキーワード数をカウント
    num_contents = sum([1 for _ in open(input_filepath)]
                       ) if limit is None else limit
    with open(input_filepath, mode='r') as f:
        for index, text in tqdm(enumerate(f), total=num_contents):
            # limitが指定されなければ全行読み込む
            if limit is not None and index >= limit:
                break
            # 英数字や記号で構成されるワードは、ブランド名の可能性が高いのでスキップする
            if checkAlnum(text):
                continue
            formatted_text = preprocessing(text)
            contents.append(formatted_text)
    print('========ファイル読み込み完了========')
    return contents


def write_contents(dirpath, contents):
    header = config.FILE_HEADER
    timestamp = datetime.datetime.now().strftime(config.TIMESTAMP_FORMAT)
    output_filepath = f'{dirpath}/result_{timestamp}.csv'
    with open(output_filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(contents)


def to_jp_keys_of_pos_counter(pos_counter):
    jp_pos_counter = {}
    for en_key in pos_counter:
        jp_key = config.POS_JP_DICT[en_key]
        jp_pos_counter[jp_key] = pos_counter[en_key]

    return jp_pos_counter


def generate_graph(dirpath, dict):
    list = dict.items()
    x, y = zip(*list)

    plt.barh(x, y, align="center")
    # 棒グラフ上に数値を書く
    for _x, _y in zip(x, y):
        plt.text(_y, _x, _y, ha='left', va='center')

    timestamp = datetime.datetime.now().strftime(config.TIMESTAMP_FORMAT)
    output_filepath = f'{dirpath}/result_{timestamp}.png'
    plt.savefig(output_filepath)
