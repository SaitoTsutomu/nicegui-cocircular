# CoCircular(共円ゲーム)

NiceGUIベースの共円を判定するゲームです。

格子をクリックして点を配置します。4つの点が同じ円周上（共円）になったらゲームオーバーです。
1直線上に4点並んだ場合も（半径∞の）共円とみなします。

![CoCircular Screenshot](https://raw.githubusercontent.com/SaitoTsutomu/nicegui-cocircular/master/images/screenshot.png)

## 遊び方

- 格子をクリックして、点を置きます。共円ができたら終了です
- 1人プレイ：何個置けるか挑戦してみましょう
- 2人以上：共円ができたら1人負けです。ただし、共円を2つ以上作ったら1人勝ちです

### 点の色

- 黒：すでに置いた点です
- 赤：現在置いた点です
- その他の色：共円を構成する点です

## 実行方法

```
% pip install nicegui-cocircular
% cocircular
```

または

```
% uv run --with nicegui-cocircular cocircular
```

自動的にWebブラウザでアプリケーションが開き、ゲームをプレイできます。

