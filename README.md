# RCJ_KickSim

---

## 概要

RCJ_KickSim は、RoboCup Junior Soccer Open 用ソレノイドキッカーの設計・最適化を目的とした物理シミュレータです。

ソレノイドの電気回路からストライカー運動、ボールとの衝突、転がり運動までを物理モデルで再現し、キック性能を予測します。

### 主な機能

- ソレノイドストライカーの運動シミュレーション
- コンデンサ放電回路のシミュレーション
- ボールとの衝突解析
- ボールの回転・転がり解析
- キック板高さの最適化
- 感度解析
- 実測データとの比較

---

## ディレクトリ構成

```text
RCJ_KickSim
│
├── src/
├── data/
├── docs/
├── output/
└── tests/
```

---

## 使用方法

リポジトリを取得します。

```bash
git clone https://github.com/ryo-robot14/RCJ_KickSim.git
cd RCJ_KickSim
```

シミュレーションを実行します。

```bash
python3 src/main.py
```

結果は

```
output/kick_height_sweep.csv
```

に出力されます。

---

## 設定変更

シミュレーション条件を変更する場合は

```
src/config.py
```

のみ編集してください。

主な設定項目

- ボール
- ストライカー
- ソレノイド
- 電源
- コンデンサ容量
- コイル抵抗
- 摩擦係数
- シミュレーション条件

通常、それ以外のソースコードを編集する必要はありません。

---

## ドキュメント

詳細な説明は

- docs/01_ProjectPlan.md
- docs/02_UsageGuide.md

をご覧ください。

---

## 開発状況

### 実装済み

- ソレノイドモデル
- コンデンサ放電モデル
- ストライカー運動
- 衝突モデル
- 転がりモデル
- キック高さ探索
- 感度解析
- CSV出力

### 今後の予定

- 実測データによるパラメータ同定
- CB1037の実測推力モデル
- GUIの実装

---

## Overview

RCJ_KickSim is a physics-based simulator for designing and optimizing solenoid kickers used in RoboCup Junior Soccer Open robots.

The simulator models the complete kicking process, from capacitor discharge and solenoid dynamics to striker motion, ball impact, and rolling behaviour.

### Features

- Solenoid striker simulation
- Capacitor-discharge circuit model
- Ball impact model
- Ball rolling simulation
- Kick-height optimization
- Sensitivity analysis
- Experimental data analysis

---

## Repository Structure

```text
RCJ_KickSim
│
├── src/
├── data/
├── docs/
├── output/
└── tests/
```

---

## Getting Started

Clone the repository.

```bash
git clone https://github.com/ryo-robot14/RCJ_KickSim.git
cd RCJ_KickSim
```

Run the simulator.

```bash
python3 src/main.py
```

Simulation results are written to

```
output/kick_height_sweep.csv
```

---

## Configuration

Most users only need to edit

```
src/config.py
```

to match their own robot.

Typical parameters include

- Ball properties
- Striker properties
- Solenoid specifications
- Supply voltage
- Capacitor capacity
- Coil resistance
- Friction coefficients
- Numerical settings

No other source files normally need to be modified.

---

## Documentation

See

- docs/01_ProjectPlan.md
- docs/02_UsageGuide.md

for detailed explanations.

---

## Current Status

### Implemented

- Solenoid model
- Capacitor-discharge model
- Striker dynamics
- Ball impact
- Rolling model
- Kick-height sweep
- Sensitivity analysis
- CSV export

### Planned

- Parameter identification
- Measured CB1037 force model
- GUI

---

## Author

**Ryo KAIJIRI**

Started in **July 2026**.