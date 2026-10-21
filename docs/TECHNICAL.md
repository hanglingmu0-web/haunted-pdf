# 実ファイルに基づく技術解説

検査日：2026年10月21日（日本時間）。すべて1ページで、通常のOptional Content Group（OCG）はありません。

| ファイル | ページ寸法（pt） | Image XObject | Widget | Stamp | 有効なタイマー |
| --- | --- | ---: | ---: | ---: | --- |
| Snow_Night_Visitor.pdf | 512 × 768 | 42 | 41 | 0 | 600 ms |
| ningyo_halloween_pumpkin.pdf | 494 × 635 | 42 | 41 | 0 | 2000 ms |
| Ningyo_Halloween_Poster.pdf | 494 × 635 | 2 | 0 | 1 | なし |

画像オブジェクト数は、相異なる絵の数とは異なります。復号した画像ストリームの内容で重複を除くと、映画ポスターは34種類、動く人形は41種類です。

## アニメーション版

ページ本体に初期画像を1枚置き、その上に全ページ大のPushbutton Widgetを41個重ねます。各Widgetの`/AP /N`はForm XObjectで、その内部に各フレームのImage XObjectがあります。画像データが通常の入力値`/V`に入っているわけではありません。

```text
Catalog
├─ Pages → 1ページ → Contents → 初期画像
│                  └─ Annots → frame_01 ... frame_41
│                                └─ AP / N → Form XObject → 画像
├─ AcroForm / Fields → 上記と同じ41個のWidget
├─ Names / JavaScript → 自動開始を含む文書レベルスクリプト
└─ OpenAction → ningyoStart();
```

Widgetは`/FT /Btn`、`/Ff 65536`（Pushbutton）。保存時の注釈フラグ`/F 38`はHidden（2）、Print（4）、NoView（32）の合計です。Hiddenが立っている初期状態では印刷もされません。再生中は`field.display`の`hidden`と`visible`を切り替えます。[AdobeのField.display定義](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/JS_API_AcroJS.html#display)

1回のtickで全Widgetを非表示にし、`step=(step+1)%48`を計算します。stepが0〜6ならページ本体のみ、7〜47ならframe_01〜41を表示します。

| 項目 | 映画ポスター | 動く人形 |
| --- | ---: | ---: |
| tick間隔 | 0.6秒 | 2秒 |
| 最初のWidgetを表示 | 4.2秒後 | 14秒後 |
| 初期画像と画素が異なる最初のWidget | frame_09：9秒後 | frame_02：16秒後 |
| 一巡 | 28.8秒 | 96秒 |

これらはコード上の予定値です。実時間の精度や滑らかさを保証しません。途中で画像が重複しているため、常に1tickごとに見た目が変わるわけではありません。

開始関数は既存タイマーを解除してから`app.setInterval()`を登録します。文書レベルスクリプトとOpenActionの両方から呼ばれますが、模擬環境では稼働タイマーが1個になることを確認しました。[AdobeのタイマーAPI](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/JS_API_AcroJS.html#setinterval)

動く人形のオブジェクト134には使われていない旧JavaScriptが残っています。現在のNamesツリーから参照されるのはオブジェクト137です。旧スクリプトを検索で見つけただけでは、現在の再生挙動を特定できません。

アニメーション版には印刷時に特定フレームへ固定する処理がありません。再生中の`display.visible`は印刷対象にもなり得るため、印刷結果は再生状態やビューアー処理に依存します。以下の印刷専用作品と区別します。

## 印刷版

| 画面用画像 | 印刷モード・注釈あり |
| --- | --- |
| ![短髪](../previews/ningyo-print-screen.png) | ![長髪](../previews/ningyo-print-output.png) |

ページ本体に画像Aを配置し、同じ矩形のStamp注釈のAppearanceに画像Bを設定します。

```text
/Subtype /Stamp
/Rect [0 0 494 635]
/F 36                 % Print 4 + NoView 32
/AP << /N ... >>      % 画像Bを描くForm XObject
```

NoViewは画面上の注釈表示を抑え、Printは印刷対象を指定します。Hiddenフラグは設定しません。印刷時にAが取り除かれるのではなく、不透明なBがページ全体を覆います。透明画像や小さな注釈に変更すると、下のAが見える場合があります。フラグ値は[PDFiumの定義](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdf_annot.h)でも確認できます。

OCGではないためレイヤーパネルに一覧表示されませんが、注釈パネル、添付ファイルパネル、解析ツールなどから構造や画像の存在に気付く可能性はあります。「通常閲覧で絶対に分からない」という保証はありません。

注釈を印刷しない設定ではBが出ず、Aが印刷されます。今回のPDFium印刷モードでも、この違いを確認しました。Acrobatの印刷設定については[Adobeの説明](https://helpx.adobe.com/acrobat/desktop/print-documents/use-secure-and-special-print-mode/print-comments.html)を参照してください。

## Chromeなどの扱い

Chrome系で利用されるPDFiumのソースには`setInterval`の実装があります。しかし、その存在だけから対象PDFがChromeで正常再生できるとは判断できません。JavaScript、フォーム、注釈再描画、ホストアプリの設定を含む実機検証が必要です。本検証のPDFium画像レンダリングはChrome UIの再生試験ではありません。[PDFium実装](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/fxjs/cjs_app.cpp)
