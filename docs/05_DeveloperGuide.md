# RCJ_KickSim Developer Guide

---

## 概要

このドキュメントは、RCJ_KickSim のソースコードを理解・拡張したい開発者向けのガイドです。

利用方法については **02_UserGuide.md** を、物理モデルについては **03_PhysicsModel.md** を参照してください。

---

# 1. プロジェクト構成

```
RCJ_KickSim/

├── src/
│   ├── config.py
│   ├── constants.py
│   ├── circuit.py
│   ├── solenoid.py
│   ├── striker.py
│   ├── ball.py
│   ├── impact.py
│   ├── rolling.py
│   ├── simulation.py
│   ├── reporting.py
│   ├── main.py
│   ├── plot_sweep.py
│   ├── analyze_trials.py
│   └── sensitivity.py
│
├── data/
│   └── measurements/
│
├── docs/
│
├── output/
│
├── README.md
└── LICENSE
```

---

# 2. 各モジュールの役割

| ファイル | 役割 |
|----------|------|
| config.py | ユーザー設定 |
| constants.py | 設定値の読み込み・定数生成 |
| circuit.py | コンデンサ放電モデル |
| solenoid.py | ソレノイド推力モデル |
| striker.py | ストライカー運動 |
| ball.py | ボール状態 |
| impact.py | 衝突モデル |
| rolling.py | 転がりモデル |
| simulation.py | シミュレーション統合 |
| reporting.py | CSV出力 |
| main.py | エントリーポイント |
| plot_sweep.py | グラフ表示 |
| analyze_trials.py | 実測解析 |
| sensitivity.py | 感度解析 |

---

# 3. シミュレーションの処理フロー

```
main.py

↓

simulation.py

↓

Circuit

↓

Solenoid

↓

Striker

↓

Impact

↓

Rolling

↓

Reporting
```

各モジュールは独立しており、入力と出力だけを共有します。

これにより、新しいモデルへの差し替えが容易になります。

---

# 4. データの流れ

```
config.py

↓

constants.py

↓

各モジュール

↓

CSV
```

すべての設定値は `config.py` に集約されます。

`constants.py` は設定値を読み込み、必要に応じて計算済み定数（例：ボールの慣性モーメント）を生成します。

各モジュールは `constants.py` の値のみを参照し、`config.py` を直接読み込まない設計になっています。

---

# 5. 新しい物理モデルを追加する

新しいモデルを追加する場合は、既存モジュールを変更するよりも、新しいファイルとして実装することを推奨します。

例

```
aerodynamics.py

thermal.py

bearing.py
```

その後

```
simulation.py
```

へ追加してください。

---

# 6. 新しい設定項目を追加する

設定値は

```
config.py
```

へ追加します。

必要に応じて

```
constants.py
```

で派生定数を作成してください。

モジュール側では `constants.py` の値を使用します。

---

# 7. コーディングルール

RCJ_KickSim では以下を推奨します。

- PEP8 に従う
- 型ヒントを使用する
- Docstring を記述する
- SI単位を使用する
- マジックナンバーを書かない
- 計算式には出典をコメントで記載する

---

# 8. 数値計算について

現在の実装

- オイラー法

将来的な候補

- Semi-Implicit Euler
- Runge-Kutta 4
- Adaptive Time Step

アルゴリズムを変更する場合は、結果の再現性を十分に確認してください。

---

# 9. テスト

物理モデルを変更した場合は、以下を確認してください。

- シミュレーションが最後まで終了する
- CSVが生成される
- 異常値が出力されない
- 既知条件で結果が再現される

可能であれば実測値との比較も行ってください。

---

# 10. 開発方針

RCJ_KickSim は以下を目標としています。

- モジュール間の独立性を保つ
- パラメータは設定ファイルへ集約する
- 実測値を優先する
- 仮定値にはコメントを残す
- 拡張しやすい設計を維持する

---

# 11. 将来の拡張予定

候補例

- RLC回路モデル
- 温度によるコイル抵抗変化
- 空気抵抗
- ボール変形
- プレート形状の最適化
- FEMとの連携
- GUI
- 3D可視化
- 自動パラメータ最適化

---

## Overview

This document is intended for developers who want to understand or extend the RCJ_KickSim source code.

For usage instructions, see **02_UserGuide.md**.

For the physical models, see **03_PhysicsModel.md**.

---

# 1. Project Structure

```
RCJ_KickSim/

├── src/
│   ├── config.py
│   ├── constants.py
│   ├── circuit.py
│   ├── solenoid.py
│   ├── striker.py
│   ├── ball.py
│   ├── impact.py
│   ├── rolling.py
│   ├── simulation.py
│   ├── reporting.py
│   ├── main.py
│   ├── plot_sweep.py
│   ├── analyze_trials.py
│   └── sensitivity.py
│
├── data/
├── docs/
├── output/
├── README.md
└── LICENSE
```

---

# 2. Module Responsibilities

| File | Purpose |
|------|---------|
| config.py | User configuration |
| constants.py | Derived constants |
| circuit.py | Capacitor discharge model |
| solenoid.py | Solenoid force model |
| striker.py | Striker dynamics |
| ball.py | Ball state |
| impact.py | Collision model |
| rolling.py | Rolling model |
| simulation.py | Simulation pipeline |
| reporting.py | CSV export |
| main.py | Entry point |
| plot_sweep.py | Plotting |
| analyze_trials.py | Experimental analysis |
| sensitivity.py | Sensitivity analysis |

---

# 3. Simulation Pipeline

```
main.py

↓

simulation.py

↓

Circuit

↓

Solenoid

↓

Striker

↓

Impact

↓

Rolling

↓

Reporting
```

Each module communicates only through its inputs and outputs, allowing easy replacement or extension.

---

# 4. Data Flow

```
config.py

↓

constants.py

↓

Simulation Modules

↓

CSV Output
```

All user-editable parameters are stored in `config.py`.

`constants.py` converts them into derived physical constants.

Simulation modules use only `constants.py`.

---

# 5. Adding a New Physical Model

New functionality should generally be implemented as a new module instead of modifying existing ones.

Examples

```
aerodynamics.py

thermal.py

bearing.py
```

Integrate the module through `simulation.py`.

---

# 6. Adding New Parameters

New parameters should first be added to

```
config.py
```

Derived quantities should be calculated inside

```
constants.py
```

Simulation modules should never access `config.py` directly.

---

# 7. Coding Style

Recommended practices

- Follow PEP 8
- Use type hints
- Write docstrings
- Use SI units
- Avoid magic numbers
- Document equations and references

---

# 8. Numerical Methods

Current implementation

- Euler integration

Possible future upgrades

- Semi-Implicit Euler
- Runge-Kutta 4
- Adaptive time stepping

Any numerical changes should preserve reproducibility.

---

# 9. Validation

Whenever a physical model is modified, verify that

- the simulation completes,
- CSV output is generated,
- no unrealistic values appear,
- previous benchmark cases remain reproducible.

Whenever possible, compare against experimental measurements.

---

# 10. Development Philosophy

RCJ_KickSim aims to

- maintain modularity,
- centralize parameters,
- prioritize measured data,
- clearly document assumptions,
- remain easy to extend.

---

# 11. Future Development

Possible future extensions include

- RLC electrical model
- Temperature-dependent coil resistance
- Aerodynamic drag
- Ball deformation
- Kick-plate optimization
- FEM integration
- GUI
- 3D visualization
- Automatic parameter optimization