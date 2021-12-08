# analyze-pos-using-ginza

自然言語ライブラリーである [GiNZA](https://megagonlabs.github.io/ginza/) を使って複数のワードの品詞を分析する。

## DEMO

下記のようなワードがあったとき

```txt
ナイロンっぽいトップス
渡せるフラワー
ピスタチオカラー
ロング
オシャレなブーツ
腕時計
セール対象商品
...
```

本ツールを実行するとワードで使われた品詞をカウントし、下記のような結果を返す。

<img src="https://user-images.githubusercontent.com/20574756/145164955-5659f923-83da-4544-9d21-56e9c3a760ee.png" width=50%>

```bash
{'形容詞': 4, '名詞': 40, '記号': 4, '接辞': 1, '固有名詞': 1, '助動詞': 2, '接置詞': 3, '数詞': 1, '代名詞': 1, '動詞': 1}
```

## Features

- GiNZA と SudachiPy を使った品詞分析
- 品詞分析の結果を棒グラフで可視化
- 大量のワードを分析したい場合、並列実行による高速化も可能

## Requirement

依存パッケージは以下の通り

- python = ">=3.9,<3.11"
- ginza = "^5.0.3"
- ja-ginza = "^5.0.0"
- emoji = "^1.6.1"
- mojimoji = "^0.0.12"
- asyncio = "^3.4.3"
- tqdm = "^4.62.3"
- neologdn = "^0.5.1"
- matplotlib = "^3.5.0"
- japanize-matplotlib = "^1.1.3"

詳細は`pyproject.toml`を参照

## Installation

poetry でパッケージを管理しているので、まだインストールしていない場合は別途インストールを行う

```bash
$ git clone https://github.com/sattosan/analyze-pos-using-ginza.git
$ cd analyze-pos-using-ginza
$ poetry install
```

## Usage

実行方法は、「通常の方法」と「並列による方法」の２パターンある。
それぞれ実行後は、`./result/main/`や`./result/thread/`に品詞分析の結果が保存される。

### 通常の実行方法

```bash
$ poetry run python src/main.py
========ファイル読み込み開始========
100%|█████████████████████████████████████████████| 30/30 [00:00<00:00, 35128.17it/s]
========ファイル読み込み完了========
========形態素解析開始========
100%|█████████████████████████████████████████████| 26/26 [00:00<00:00, 99.57it/s]
{'形容詞': 4, '名詞': 40, '記号': 4, '接辞': 1, '固有名詞': 1, '助動詞': 2, '接置詞': 3, '数詞': 1, '代名詞': 1, '動詞': 1}
========形態素解析完了========
実行時間: 0.24016714096069336s
```

### 並列による実行方法

```bash
$ poetry run python src/thread-main.py
========ファイル読み込み開始========
100%|█████████████████████████████████████████████| 30/30 [00:00<00:00, 35128.17it/s]
========ファイル読み込み完了========
========形態素解析開始========
100%|█████████████████████████████████████████████| 26/26 [00:00<00:00, 99.57it/s]
{'形容詞': 4, '名詞': 40, '記号': 4, '接辞': 1, '固有名詞': 1, '助動詞': 2, '接置詞': 3, '数詞': 1, '代名詞': 1, '動詞': 1}
========形態素解析完了========
実行時間: 0.2710714340209961s
```

※ 分析するワード数が少ないと、並列化によるオーバーヘッドによって通常時より動作が遅くなる可能性がある
