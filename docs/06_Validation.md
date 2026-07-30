# RCJ_KickSim Validation Guide

---

## 概要

このドキュメントでは、RCJ_KickSim の物理モデルを実機によって校正・検証する方法について説明します。

シミュレーションはデータシートや物理法則に基づいて構築されていますが、一部のパラメータは仮定値です。

設計に利用する前に、実機で校正することを推奨します。

---

# 1. 検証の目的

本プロジェクトの検証では、以下を確認することを目的としています。

- シミュレーション結果が実機と一致するか
- 仮定値を実測値へ置き換える
- モデルの誤差を定量化する
- 将来の設計精度を向上させる

---

# 2. 校正優先順位

推奨する校正順序は以下の通りです。

| 優先度 | 項目 | 理由 |
|--------|------|------|
| ★★★★★ | 床の滑り摩擦係数 | 停止距離への影響が大きい |
| ★★★★★ | 転がり減速度 | 停止距離への影響が大きい |
| ★★★★☆ | ストライカー・ボール反発係数 | 初速度・スピンへ影響 |
| ★★★☆☆ | コイルインダクタンス | 電流波形へ影響 |
| ★★★☆☆ | 磁気飽和ニー電流 | 推力へ影響 |
| ★★☆☆☆ | トリガーパルス幅 | 通電時間へ影響 |

---

# 3. 実測データの保存

実測データは

```
data/measurements/
```

へ保存します。

例

```
kick_trials.csv
```

必要に応じて

```
coil_current.csv

force_curve.csv

rolling_test.csv
```

などを追加してください。

---

# 4. キック高さの検証

## 方法

1. プレート高さを固定する
2. 同じ条件で複数回キックする
3. 停止距離を測定する
4. CSVへ記録する

推奨

- 5回以上
- 同じボール
- 同じ電圧
- 同じフィールド

---

## CSV例

|height_from_floor_mm|roll_distance_m|
|---|---|
|30|4.18|
|30|4.12|
|30|4.26|

---

## 解析

```bash
python3 src/analyze_trials.py data/measurements/kick_trials.csv
```

平均値と標準偏差から最適高さを求めます。

---

# 5. ストライカー速度の測定

## 推奨方法

- 高速度カメラ
- フォトインタラプタ
- レーザーゲート

測定した速度は

```bash
python3 src/main.py --striker-speed 5.82
```

のように直接入力できます。

これにより電気モデルを使わずに衝突モデルを検証できます。

---

# 6. コイル電流の測定

目的

- コイルインダクタンスの推定
- RLCモデルの構築

推奨機材

- オシロスコープ
- シャント抵抗

測定結果から

```
COIL_INDUCTANCE_H
```

を書き換えます。

---

# 7. 推力曲線の測定

データシートには24V時の推力しか掲載されていません。

48V動作では

- 飽和
- 発熱

の影響があるため、可能であれば実測を推奨します。

測定結果から

```
SATURATION_KNEE_CURRENT_A
```

を更新します。

---

# 8. 反発係数の測定

必要機材

- 高速度カメラ

測定項目

- 衝突前速度
- 衝突後速度

そこから反発係数を算出します。

更新項目

```
STRIKER_BALL_RESTITUTION
```

---

# 9. 床面の校正

測定する項目

- 滑り距離
- 滑り時間
- 転がり距離
- 停止時間

更新項目

```
SLIDING_FRICTION_COEFFICIENT

ROLLING_DECELERATION_M_S2
```

この2つは停止距離に最も大きな影響を与えます。

---

# 10. 感度解析

実測前に

```bash
python3 src/sensitivity.py
```

を実行することで、

- どのパラメータを優先して測定すべきか
- 不確かさが設計へ与える影響

を確認できます。

---

# 11. モデル更新手順

校正時は以下の流れを推奨します。

```
実測

↓

CSV保存

↓

パラメータ更新

↓

main.py

↓

実測との比較

↓

誤差評価

↓

必要なら再校正
```

---

# 12. 検証完了の目安

シミュレーションが以下を満たすことを目標とします。

- 最適高さが実機と一致する
- 初速度が実機と一致する
- スピン量が実機と一致する
- 停止距離が実機と一致する
- 実測結果を再現できる

---

## Overview

This document describes how to validate and calibrate the RCJ_KickSim physical models using experimental measurements.

Although the simulator is based on physical principles and manufacturer datasheets, several parameters are currently estimated and should be replaced with measured values.

---

# 1. Objectives

The validation process aims to

- verify agreement between simulation and experiment,
- replace estimated parameters with measurements,
- quantify model error,
- improve future prediction accuracy.

---

# 2. Calibration Priority

Recommended order of calibration.

| Priority | Parameter | Reason |
|----------|-----------|--------|
| ★★★★★ | Sliding friction coefficient | Strong influence on stopping distance |
| ★★★★★ | Rolling deceleration | Strong influence on stopping distance |
| ★★★★☆ | Restitution coefficient | Influences launch speed and spin |
| ★★★☆☆ | Coil inductance | Influences current waveform |
| ★★★☆☆ | Saturation knee current | Influences solenoid force |
| ★★☆☆☆ | Trigger pulse duration | Influences energizing time |

---

# 3. Measurement Data

Experimental data should be stored in

```
data/measurements/
```

Example files

```
kick_trials.csv

coil_current.csv

force_curve.csv

rolling_test.csv
```

---

# 4. Kick Height Validation

Procedure

1. Fix the kick height.
2. Perform multiple kicks.
3. Measure the stopping distance.
4. Record the results in CSV.

Recommended conditions

- At least five trials
- Same ball
- Same voltage
- Same playing surface

Analyze using

```bash
python3 src/analyze_trials.py data/measurements/kick_trials.csv
```

---

# 5. Measuring Striker Speed

Recommended methods

- High-speed camera
- Photo interrupter
- Laser gate

Use the measured value directly

```bash
python3 src/main.py --striker-speed 5.82
```

This allows validation of the impact model independently of the electrical model.

---

# 6. Measuring Coil Current

Purpose

- Estimate coil inductance
- Develop an RLC electrical model

Recommended equipment

- Oscilloscope
- Shunt resistor

Update

```
COIL_INDUCTANCE_H
```

after measurement.

---

# 7. Measuring Force Curve

The CB1037 datasheet provides force data only at the rated operating condition.

For 48 V operation, magnetic saturation and heating may change the force characteristics.

Experimental measurements can be used to update

```
SATURATION_KNEE_CURRENT_A
```

---

# 8. Measuring Restitution

Recommended equipment

- High-speed camera

Measure

- pre-impact velocity,
- post-impact velocity,

to estimate the coefficient of restitution.

Update

```
STRIKER_BALL_RESTITUTION
```

---

# 9. Surface Calibration

Measure

- sliding distance,
- sliding time,
- rolling distance,
- stopping time.

Update

```
SLIDING_FRICTION_COEFFICIENT

ROLLING_DECELERATION_M_S2
```

These parameters have the greatest influence on stopping-distance prediction.

---

# 10. Sensitivity Analysis

Before collecting measurements, run

```bash
python3 src/sensitivity.py
```

to identify

- which parameters should be measured first,
- which assumptions contribute most to uncertainty.

---

# 11. Calibration Workflow

Recommended workflow

```
Experiment

↓

Save CSV

↓

Update parameters

↓

Run main.py

↓

Compare with experiment

↓

Evaluate error

↓

Repeat if necessary
```

---

# 12. Validation Targets

The simulator should ultimately reproduce

- optimal kick height,
- ball launch speed,
- ball spin,
- stopping distance,
- overall experimental behavior.