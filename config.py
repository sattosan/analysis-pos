FILE_HEADER = ['keyword', 'token_pos']
INPUT_FILEPATH = 'keywords.csv'
NORMAL_OUTPUT_DIRPATH = './result/main'
THREAD_OUTPUT_DIRPATH = './result/thread'
TIMESTAMP_FORMAT = '%Y%m%d%H%M%S'
MAX_WORKERS = 5
THREAD_TIMEOUT = 3
POS_JP_DICT = {
    'NOUN': '名詞',
    'PROPN': '固有名詞',
    'VERB': '動詞',
    'ADJ': '形容詞',
    'ADV': '副詞',
    'INTJ': '間投詞',
    'PRON': '代名詞',
    'NUM': '数詞',
    'AUX': '助動詞',
    'CONJ': '接続詞',
    'SCONJ': '従属接続詞',
    'DET': '限定詞',
    'ADP': '接置詞',
    'PART': '接辞',
    'PUNCT': '句読点',
    'SYM': '記号',
    'X': 'その他'
}
