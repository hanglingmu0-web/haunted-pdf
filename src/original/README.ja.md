# 有効なJavaScriptの抽出

[English](README.md) | 日本語

`snow.js`と`ningyo-animation.js`は、それぞれの原本PDFの`Names / JavaScript`から参照されるスクリプトを抽出したものです。OpenActionはいずれも`ningyoStart();`です。

PDF内の値を保つため、映画ポスター側も元の`ningyo`という変数名・関数名をそのまま掲載しています。未使用の旧スクリプトは実行対象のソースに混ぜていません。

再構築時には`extract`が原本から`work/assets/`へ抽出し直したスクリプトを使います。このフォルダーは閲覧用です。
