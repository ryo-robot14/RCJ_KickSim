# RCJ_KickSim Configuration Reference

---

## 概要

このドキュメントでは、`src/config.py` に定義されているすべての設定項目について説明します。

RCJ_KickSim の動作は、基本的に **`config.py` を編集するだけ**で変更できます。

プログラム本体を変更する必要はありません。

---

# 1. ボール設定

## BALL_MASS_KG

ボールの質量です。

```python
BALL_MASS_KG = 0.04593
```

単位

```
kg
```

RCJ Soccer Open で一般的に使用されるゴルフボールの質量です。

---

## BALL_RADIUS_M

ボール半径です。

```python
BALL_RADIUS_M = 0.02135
```

単位

```
m
```

ボール径を変更する場合のみ変更してください。

---

# 2. ストライカー設定

## STRIKER_MASS_KG

ストライカー全体の質量です。

```python
STRIKER_MASS_KG = 0.026
```

単位

```
kg
```

L字プレートを含めた質量を入力します。

---

## STRIKER_STROKE_M

ストローク長です。

```python
STRIKER_STROKE_M = 0.010
```

単位

```
m
```

ソレノイドの実ストロークを入力してください。

---

# 3. 電源設定

## INITIAL_VOLTAGE_V

コンデンサ初期電圧です。

```python
INITIAL_VOLTAGE_V = 48.0
```

単位

```
V
```

昇圧後の電圧を設定します。

---

## CAPACITOR_F

コンデンサ容量です。

```python
CAPACITOR_F = 4000e-6
```

単位

```
F
```

複数個並列接続する場合は合計容量を入力してください。

---

# 4. コイル設定

## COIL_RESISTANCE_OHM

コイル抵抗です。

```python
COIL_RESISTANCE_OHM = 10.0
```

単位

```
Ω
```

データシート値または実測値を入力してください。

---

## COIL_INDUCTANCE_H

コイルインダクタンスです。

```python
COIL_INDUCTANCE_H = 0.0
```

単位

```
H
```

現在は未測定のため0となっています。

測定後はこの値を書き換えるだけで利用できます。

---

## STATIC_FORCE_CURVE_VOLTAGE_V

推力曲線取得時の印加電圧です。

```python
STATIC_FORCE_CURVE_VOLTAGE_V = 24.0
```

単位

```
V
```

CB1037データシートの条件です。

通常変更する必要はありません。

---

## SATURATION_KNEE_CURRENT_A

磁気飽和ニー電流です。

```python
SATURATION_KNEE_CURRENT_A = 3.6
```

単位

```
A
```

推力の飽和開始電流です。

現在は仮定値です。

---

## TRIGGER_PULSE_DURATION_S

通電時間です。

```python
TRIGGER_PULSE_DURATION_S = 0.5
```

単位

```
s
```

現在は実質無制限となっています。

ワンショット回路の実測後に変更してください。

---

# 5. 衝突設定

## STRIKER_BALL_RESTITUTION

反発係数です。

```python
STRIKER_BALL_RESTITUTION = 0.65
```

単位

```
なし
```

現在は仮定値です。

高速度カメラによる校正を推奨します。

---

# 6. 床設定

## SLIDING_FRICTION_COEFFICIENT

滑り摩擦係数です。

```python
SLIDING_FRICTION_COEFFICIENT = 0.35
```

RCJフィールド上で測定してください。

---

## ROLLING_DECELERATION_M_S2

純転がり減速度です。

```python
ROLLING_DECELERATION_M_S2 = 1.00
```

単位

```
m/s²
```

実測による更新を推奨します。

---

# 7. 数値計算設定

## TIME_STEP_S

時間刻みです。

```python
TIME_STEP_S = 1e-5
```

小さくすると精度は向上しますが、計算時間が長くなります。

---

## KICK_HEIGHT_STEP_M

高さ探索の刻みです。

```python
KICK_HEIGHT_STEP_M = 0.0001
```

0.1 mm刻みです。

---

## MAX_STRIKER_SIMULATION_TIME_S

ストライカーシミュレーションの最大時間です。

```python
MAX_STRIKER_SIMULATION_TIME_S = 1.0
```

無限ループ防止用です。

通常変更する必要はありません。

---

# 8. 推奨設定変更例

## 12Vソレノイド

```python
INITIAL_VOLTAGE_V = 12.0
```

---

## 24Vソレノイド

```python
INITIAL_VOLTAGE_V = 24.0
```

---

## 48V昇圧

```python
INITIAL_VOLTAGE_V = 48.0
```

---

## 容量変更

2200μF×2

```python
CAPACITOR_F = 4400e-6
```

1000μF×4

```python
CAPACITOR_F = 4000e-6
```

---

## ボール変更

重量だけ変更

```python
BALL_MASS_KG = 0.0465
```

半径も変更

```python
BALL_RADIUS_M = ...
```

---

# 9. 編集するべきファイル

通常ユーザーが編集するファイルは

```
config.py
```

のみです。

それ以外のファイルはシミュレーション本体であり、変更する必要はありません。

---

## Overview

This document describes every configurable parameter in `src/config.py`.

For most users, **editing `config.py` is the only required customization**.

No changes to the simulator source code are normally necessary.

---

# 1. Ball Parameters

## BALL_MASS_KG

Ball mass.

```python
BALL_MASS_KG = 0.04593
```

Unit

```
kg
```

---

## BALL_RADIUS_M

Ball radius.

```python
BALL_RADIUS_M = 0.02135
```

Unit

```
m
```

---

# 2. Striker Parameters

## STRIKER_MASS_KG

Total striker mass including the kick plate.

```python
STRIKER_MASS_KG = 0.026
```

---

## STRIKER_STROKE_M

Stroke length.

```python
STRIKER_STROKE_M = 0.010
```

Unit

```
m
```

---

# 3. Electrical Parameters

## INITIAL_VOLTAGE_V

Initial capacitor voltage.

```python
INITIAL_VOLTAGE_V = 48.0
```

---

## CAPACITOR_F

Capacitance.

```python
CAPACITOR_F = 4000e-6
```

Unit

```
F
```

---

# 4. Coil Parameters

## COIL_RESISTANCE_OHM

Coil resistance.

```python
COIL_RESISTANCE_OHM = 10.0
```

---

## COIL_INDUCTANCE_H

Coil inductance.

```python
COIL_INDUCTANCE_H = 0.0
```

Currently assumed because no measurement is available.

---

## STATIC_FORCE_CURVE_VOLTAGE_V

Voltage used to obtain the datasheet force curve.

```python
STATIC_FORCE_CURVE_VOLTAGE_V = 24.0
```

Normally this should not be modified.

---

## SATURATION_KNEE_CURRENT_A

Magnetic saturation knee current.

```python
SATURATION_KNEE_CURRENT_A = 3.6
```

Currently an estimated value.

---

## TRIGGER_PULSE_DURATION_S

Trigger pulse duration.

```python
TRIGGER_PULSE_DURATION_S = 0.5
```

Currently long enough to behave as unlimited conduction.

---

# 5. Impact Parameters

## STRIKER_BALL_RESTITUTION

Coefficient of restitution.

```python
STRIKER_BALL_RESTITUTION = 0.65
```

Currently estimated.

---

# 6. Surface Parameters

## SLIDING_FRICTION_COEFFICIENT

Sliding friction coefficient.

```python
SLIDING_FRICTION_COEFFICIENT = 0.35
```

---

## ROLLING_DECELERATION_M_S2

Rolling deceleration.

```python
ROLLING_DECELERATION_M_S2 = 1.00
```

---

# 7. Numerical Parameters

## TIME_STEP_S

Simulation time step.

```python
TIME_STEP_S = 1e-5
```

---

## KICK_HEIGHT_STEP_M

Kick-height sweep resolution.

```python
KICK_HEIGHT_STEP_M = 0.0001
```

---

## MAX_STRIKER_SIMULATION_TIME_S

Maximum striker simulation time.

```python
MAX_STRIKER_SIMULATION_TIME_S = 1.0
```

Safety limit to prevent infinite loops.

---

# 8. Example Configurations

### 12 V System

```python
INITIAL_VOLTAGE_V = 12.0
```

### 24 V System

```python
INITIAL_VOLTAGE_V = 24.0
```

### 48 V Boost System

```python
INITIAL_VOLTAGE_V = 48.0
```

### Capacitor Bank

2200 μF × 2

```python
CAPACITOR_F = 4400e-6
```

1000 μF × 4

```python
CAPACITOR_F = 4000e-6
```

---

# 9. Which File Should Users Edit?

For almost all use cases, users only need to modify

```
src/config.py
```

All remaining source files implement the simulator itself and generally should not be edited.