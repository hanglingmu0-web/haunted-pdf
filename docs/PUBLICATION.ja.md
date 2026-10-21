# GitHub公開情報

[English](PUBLICATION.md) | 日本語

公開先：[hanglingmu0-web/haunted-pdf](https://github.com/hanglingmu0-web/haunted-pdf)

公開日：2026年10月21日（日本時間）。公開ブランチは`main`です。

## note記事に貼るリンク

- [リポジトリ・技術解説の入口](https://github.com/hanglingmu0-web/haunted-pdf)
- [映画ポスターのPDF](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/samples/Snow_Night_Visitor.pdf)
- [動く日本人形のPDF](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/samples/ningyo_halloween_pumpkin.pdf)
- [印刷で変化する日本人形のPDF](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/samples/Ningyo_Halloween_Poster.pdf)
- [検証結果](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/docs/VALIDATION.ja.md)
- [個人情報検査](https://github.com/hanglingmu0-web/haunted-pdf/blob/main/docs/PRIVACY.ja.md)

PDFのページを開いたら、ダウンロードして対応ビューアーで開いてください。GitHubのプレビュー上での再生を案内するものではありません。

## 公開内容

作者提供の原本PDF3点、プレビュー画像、再構築・検査コード、検証結果、技術解説、note記事の修正案を公開しています。原本PDFの合計は46,265,955バイトで、SHA-256は`SHA256SUMS.txt`に記録しています。

作業ログ、ローカルの絶対パス、仮想環境、抽出した中間画像は収録していません。コミットにはGitHubのnoreplyアドレスを使用しています。

## 原本の確認

```sh
python src/verify_hashes.py
```

再構築方法は[README](../README.ja.md)、ビューアーでの手動確認方法は[検証結果](VALIDATION.ja.md)を参照してください。GitHub Actionsの自動検証は画像一致・構造・模擬タイマーを対象とし、AcrobatやChromeの実機試験ではありません。

## 現在の利用条件と検証範囲

ライセンスは未指定です。架空の映画ポスターは公式作品・公式告知ではありません。PDF内の個人情報検査と、制作素材の権利関係の確認は別の作業です。実ビューアーでの確認結果は、実施後に環境・バージョンとともに追記します。
