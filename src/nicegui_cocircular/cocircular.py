"""共円

格子をクリックして点を作成していき、4点が同心円になったらゲームオーバー
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import ClassVar

import numpy as np
from nicegui import ui

type Point = tuple[int, int]
LAST_CLICKED_COLOR = -1


@dataclass(frozen=True)
class CenterRadius:
    """外心の中心と半径の2乗"""

    center_x: Fraction
    center_y: Fraction
    radius2: Fraction

    def __repr__(self) -> str:
        """文字列化"""
        return f"({float(self.center_x):.2f}, {float(self.center_y):.2f}): {self.radius2**0.5:.2f}"


def get_excenter(p0_: Point, p1_: Point, p2_: Point) -> CenterRadius:  # noqa: PLR0914
    """外心の中心と半径の2乗を返す"""
    # 計算しやすくするため多次元配列に変換
    p0 = np.array(p0_, dtype=np.int64)
    p1 = np.array(p1_, dtype=np.int64)
    p2 = np.array(p2_, dtype=np.int64)
    if (p0 == p1).all() or (p1 == p2).all() or (p2 == p0).all():
        msg = "Three points must be different."
        raise ValueError(msg)
    # 差分のノルム
    v01 = (p0 - p1) @ (p0 - p1)
    v12 = (p1 - p2) @ (p1 - p2)
    v20 = (p2 - p0) @ (p2 - p0)
    # 中間結果
    w01 = v01 * (v12 + v20 - v01)
    w12 = v12 * (v20 + v01 - v12)
    w20 = v20 * (v01 + v12 - v20)
    p0x, p0y = map(int, p0)
    w = int(w01 + w12 + w20)
    if w == 0:
        if p0[0] == p1[0]:  # xが同じ
            return CenterRadius(Fraction(-1), Fraction(0), Fraction(p0x))
        # yが同じ
        return CenterRadius(Fraction(0), Fraction(-1), Fraction(p0y))
    px, py = map(int, w12 * p0 + w20 * p1 + w01 * p2)
    # 中心
    cx = Fraction(px, w)
    cy = Fraction(py, w)
    # 半径の2乗
    radius2 = (cx - p0x) ** 2 + (cy - p0y) ** 2
    return CenterRadius(cx, cy, radius2)


class Square(ui.button):
    """マス"""

    colors: ClassVar[dict[int, str]] = {0: "black", 1: "blue", 2: "green", 3: "orange", 4: "yellow", 5: "pink"}

    def __init__(self, game: "Game", y: int, x: int) -> None:
        """初期化"""
        super().__init__()
        self.game = game
        self.y = y
        self.x = x
        self.on("click", lambda: self.game.click(y, x))
        self.classes("w-10 h-10 bg-white")
        self.build()

    def build(self) -> None:
        """構築"""
        self.text = self.icon = None
        self.props("text-color=white")
        c = self.game.circular[self.y, self.x]
        color = self.colors.get(c, "red")
        self.props(f"text-color={color}")
        text = "⬤" if self.game.grid[self.y, self.x] else "╋"
        self.text = text


class Game:
    """ゲーム"""

    def __init__(self, *, grid_size: int) -> None:
        """初期化"""
        self.cache: dict[CenterRadius, set[Point]] = {}
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=bool)
        self.circular = np.full_like(self.grid, 0, dtype=np.int8)
        with ui.row():
            ui.button("Restart", on_click=self.restart)
            self.label = ui.label()
        with ui.grid(columns=grid_size).classes("gap-0"):
            self.squares = [Square(self, y, x) for y in range(grid_size) for x in range(grid_size)]
        self.restart()

    def restart(self) -> None:
        """再ゲーム"""
        self.cache.clear()
        self.grid.fill(0)
        self.circular.fill(0)
        self.refresh()

    def refresh(self) -> None:
        """再描画"""
        for square in self.squares:
            square.build()

    def click(self, y: int, x: int) -> None:
        """点を置く"""
        if not self.grid[y, x] and not self.circular.any():
            self.judge(y, x)
            self.grid[y, x] = True
            self.refresh()

    def judge(self, y: int, x: int) -> None:
        """判定"""
        found = set()
        indexes = [(j, i) for j, i in product(range(self.grid_size), range(self.grid_size)) if self.grid[j, i]]
        for k, (y0, x0) in enumerate(indexes):
            for y1, x1 in indexes[k + 1 :]:
                key = get_excenter((y0, x0), (y1, x1), (y, x))
                if key not in self.cache:
                    self.cache[key] = lst = set()
                else:
                    found.add(key)
                    lst = self.cache[key]
                    for j, i in lst:
                        self.circular[j, i] = len(found)
                lst.add((y0, x0))
                lst.add((y1, x1))
                lst.add((y, x))
        if found:
            self.circular[y, x] = LAST_CLICKED_COLOR
            ui.notify("CoCircular!", type="positive")


def run_game(*, grid_size: int = 10, port: int | None = None) -> None:
    """ゲーム実行"""
    Game(grid_size=grid_size)
    ui.run(title="CoCircular", reload=False, port=port)
