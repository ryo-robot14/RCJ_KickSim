# RCJ_KickSim User Guide

---

## 概要

RCJ_KickSim のインストール方法、基本的な使い方、および各スクリプトの役割を説明します。

本書は「シミュレータを使う人」のためのガイドです。

物理モデルの詳細については **03_PhysicsModel.md**、設定項目については **04_Configuration.md**、開発者向け情報については **05_DeveloperGuide.md** を参照してください。

---

# 1. インストール

## 必要環境

- Python 3.11以上（推奨：3.14）
- Git
- VSCode（推奨）

---

## リポジトリの取得

```bash
git clone https://github.com/ryo-robot14/RCJ_KickSim.git
cd RCJ_KickSim
```

---

## 動作確認

```bash
python3 src/main.py
```

正常に実行されると

```
output/kick_height_sweep.csv
```

が生成されます。

---

# 2. ディレクトリ構成

```
RCJ_KickSim/

src/
data/
docs/
output/

README.md
LICENSE
```

---

# 3. 基本的な使い方

通常は

```
src/config.py
```

のみ編集します。

その後

```bash
python3 src/main.py
```

を実行してください。

結果は

```
output/
```

へ保存されます。

---

# 4. 各スクリプト

## main.py

理論シミュレーションを実行します。

```bash
python3 src/main.py
```

---

### オプション

| オプション | 説明 |
|------------|------|
| --csv | 出力CSV |
| --striker-speed | 実測速度を使用 |
| --coil-inductance | コイルLを変更 |
| --trigger-duration | 通電時間変更 |
| --saturation-knee-current | 飽和電流変更 |

---

## plot_sweep.py

CSVをグラフ表示します。

```bash
python3 src/plot_sweep.py
```

---

## analyze_trials.py

実測データを解析します。

```bash
python3 src/analyze_trials.py data/measurements/kick_trials.csv
```

---

## sensitivity.py

モンテカルロ感度解析を実行します。

```bash
python3 src/sensitivity.py
```

---

# 5. 出力CSV

出力されるCSVには以下が含まれます。

|列名|内容|
|---|---|
|height_from_floor_mm|キック高さ|
|ball_release_speed_m_s|初速度|
|ball_angular_velocity_rad_s|角速度|
|sliding_distance_m|滑り距離|
|rolling_distance_m|転がり距離|
|total_distance_m|停止距離|

---

# 6. 推奨ワークフロー

① `config.py` を編集

↓

② `main.py`

↓

③ CSV確認

↓

④ `plot_sweep.py`

↓

⑤ 実機測定

↓

⑥ `analyze_trials.py`

↓

⑦ 必要なら `sensitivity.py`

---

## Overview

This guide explains how to install and use RCJ_KickSim.

It is intended for simulator users.

For implementation details, see **03_PhysicsModel.md**.

For configuration parameters, see **04_Configuration.md**.

For developers, see **05_DeveloperGuide.md**.

---

# 1. Installation

## Requirements

- Python 3.11 or newer (3.14 recommended)
- Git
- VSCode (recommended)

---

## Clone Repository

```bash
git clone https://github.com/ryo-robot14/RCJ_KickSim.git
cd RCJ_KickSim
```

---

## Verify Installation

```bash
python3 src/main.py
```

The simulator should generate

```
output/kick_height_sweep.csv
```

---

# 2. Directory Structure

```
RCJ_KickSim/

src/
data/
docs/
output/

README.md
LICENSE
```

---

# 3. Basic Usage

Normally, only

```
src/config.py
```

needs to be edited.

Run

```bash
python3 src/main.py
```

Results will be written to

```
output/
```

---

# 4. Scripts

## main.py

Runs the complete simulation.

```bash
python3 src/main.py
```

---

### Options

|Option|Description|
|-------|-----------|
|--csv|Output CSV|
|--striker-speed|Measured striker speed|
|--coil-inductance|Override coil inductance|
|--trigger-duration|Override trigger duration|
|--saturation-knee-current|Override saturation current|

---

## plot_sweep.py

Plots CSV results.

```bash
python3 src/plot_sweep.py
```

---

## analyze_trials.py

Analyzes experimental data.

```bash
python3 src/analyze_trials.py data/measurements/kick_trials.csv
```

---

## sensitivity.py

Runs Monte Carlo sensitivity analysis.

```bash
python3 src/sensitivity.py
```

---

# 5. Output CSV

The generated CSV includes

|Column|Description|
|------|-----------|
|height_from_floor_mm|Kick height|
|ball_release_speed_m_s|Ball speed|
|ball_angular_velocity_rad_s|Angular velocity|
|sliding_distance_m|Sliding distance|
|rolling_distance_m|Rolling distance|
|total_distance_m|Total distance|

---

# 6. Recommended Workflow

Edit `config.py`

↓

Run `main.py`

↓

Check CSV

↓

Run `plot_sweep.py`

↓

Perform experiments

↓

Run `analyze_trials.py`

↓

Run `sensitivity.py` if necessary