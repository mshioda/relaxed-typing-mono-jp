[Read me in English](./README.md)

# Relaxed Typing Mono
Relaxed Typing Mono は、Source Code Pro と Noto Sans JP の派生フォントです。英数字は Source Code Pro、漢字は Noto Sans JP をもとにしています。

このフォントでは、漢字は英数字のちょうど 2 倍の幅になっています。また、「■」など、ときどき半角文字として扱われる記号も全角になっています。

## ダウンロード
フォントは[こちら](https://github.com/mshioda/relaxed-typing-mono/releases)からダウンロードできます。

## 表示例
#### Windows 上のメモ帳の場合
![スクリーンショット](./images/screenshot-notepad.png)

#### macOS 上の Atom の場合
![スクリーンショット](./images/screenshot-atom.png)

## 生成の仕方
1. Source Code Pro（TTF）と Noto Sans JP（OTF）をダウンロードしてください
2. それらを `resources` ディレクトリに入れます
3. `script.py` を実行します（`fontforge` Python ライブラリが必要です）
