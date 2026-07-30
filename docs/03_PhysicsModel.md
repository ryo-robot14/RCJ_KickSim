# RCJ_KickSim Physics Model

---

## 概要

このドキュメントでは、RCJ_KickSim が採用している物理モデルについて説明します。

RCJ_KickSim は、ソレノイドキッカーによるボールの発射から停止までを、複数の独立した物理モデルへ分割して計算しています。

各モデルは可能な限り実測値やデータシートに基づいて構築されていますが、一部の値は公開データが存在しないため仮定値を使用しています。

利用者が変更するパラメータは **`src/config.py`** に集約されています。

---

# 1. シミュレーション全体の流れ

シミュレーションは以下の順番で実行されます。

```
config.py
      │
      ▼
Circuit
      │
      ▼
Solenoid
      │
      ▼
Striker
      │
      ▼
Impact
      │
      ▼
Rolling
      │
      ▼
Reporting
```

各モジュールは独立しており、新しいモデルへの置き換えや機能追加が容易な構成になっています。

---

# 2. ボールモデル

ボールは一様な剛体球としてモデル化しています。

| 項目 | 値 |
|------|----|
| 質量 | 45.93 g |
| 半径 | 21.35 mm |
| 慣性モーメント | (2/5)mr² |

慣性モーメントはプログラム内で自動計算されます。

空気抵抗やボールの変形は現在考慮していません。

---

# 3. ストライカーモデル

ストライカーはL字キックプレートを含めた質点として扱います。

| 項目 | 値 |
|------|----|
| 質量 | 26 g |
| ストローク | 10 mm |

ストライカーの運動は

```
F = ma
```

をオイラー法で時間積分して求めます。

各時間ステップで

- 加速度
- 速度
- 位置

を更新します。

---

# 4. コンデンサ放電モデル

電源は48Vまで昇圧したコンデンサとしてモデル化しています。

| 項目 | 値 |
|------|----|
| 初期電圧 | 48 V |
| コンデンサ容量 | 4000 μF |

現在は

```
I = V / R
```

を用いた簡易RC放電モデルです。

コイルインダクタンスは未測定のため現在は0 Hとしています。

将来的には

- コイルインダクタンス
- 配線抵抗
- ESR

を含むRLC過渡応答モデルへ拡張可能です。

---

# 5. ソレノイドモデル

ソレノイド推力はCB1037データシートに掲載されている推力曲線を利用しています。

データシートには

- ストローク位置
- 推力

の関係が示されているため、現在位置に応じて線形補間を行っています。

さらに実際の電流値を考慮するため、

```
F(x,I)
```

として推力をスケーリングします。

磁気飽和は

```
tanh()
```

関数で近似しています。

これにより高電流時でも推力が無限に増加しないようになっています。

---

# 6. 衝突モデル

ストライカーとボールの衝突では

- 運動量保存
- 反発係数

を利用します。

入力

- ストライカー速度
- 接触高さ

出力

- ボール初速度
- ボール角速度

となります。

反発係数は現在仮定値です。

今後、高速度カメラによる実測を予定しています。

---

# 7. 転がりモデル

ボール運動は

1. 滑り
2. 純転がり

の2段階に分けて計算します。

### 滑り区間

使用する値

- 滑り摩擦係数

計算する値

- 滑り時間
- 滑り距離

---

### 純転がり区間

使用する値

- 一定減速度

計算する値

- 転がり距離
- 停止時間

最終的に停止距離を算出します。

---

# 8. 数値積分

現在はオイラー法を使用しています。

設定値

| 項目 | 値 |
|------|----|
| 時間刻み | 0.01 ms |
| 高さ刻み | 0.1 mm |

これらは `config.py` から変更できます。

---

# 9. モデル全体の計算手順

1. 設定値を読み込む
2. コンデンサ放電を計算
3. ソレノイド推力を計算
4. ストライカー運動を計算
5. 衝突計算
6. 滑り計算
7. 転がり計算
8. CSVへ出力

---

# 10. 現在の仮定

現在、以下のパラメータは仮定値です。

| パラメータ | 理由 |
|------------|------|
| コイルインダクタンス | データなし |
| 磁気飽和ニー電流 | データなし |
| 反発係数 | 未測定 |
| 滑り摩擦係数 | 未測定 |
| 転がり減速度 | 未測定 |

感度解析を利用することで、どの仮定が結果へ最も影響するかを確認できます。

---

## Overview

This document describes the physical models implemented in RCJ_KickSim.

The simulator divides the complete kicking process into several independent physical models, from capacitor discharge to the ball stopping on the field.

Whenever possible, the models are based on measurements or manufacturer datasheets. Parameters without available data are currently estimated.

All user-editable parameters are stored in **`src/config.py`**.

---

# 1. Simulation Pipeline

The simulation follows the sequence below.

```
config.py
      │
      ▼
Circuit
      │
      ▼
Solenoid
      │
      ▼
Striker
      │
      ▼
Impact
      │
      ▼
Rolling
      │
      ▼
Reporting
```

Each module is independent, making it easy to replace or extend individual models.

---

# 2. Ball Model

The ball is modeled as a rigid uniform sphere.

| Item | Value |
|------|-------|
| Mass | 45.93 g |
| Radius | 21.35 mm |
| Moment of inertia | (2/5)mr² |

The moment of inertia is calculated automatically.

Aerodynamic drag and ball deformation are not currently modeled.

---

# 3. Striker Model

The striker, including the L-shaped kick plate, is modeled as a point mass.

| Item | Value |
|------|-------|
| Mass | 26 g |
| Stroke | 10 mm |

The equation

```
F = ma
```

is integrated using the Euler method.

Position, velocity, and acceleration are updated at every time step.

---

# 4. Capacitor Discharge Model

The power source is modeled as a capacitor charged to 48 V.

| Item | Value |
|------|-------|
| Initial voltage | 48 V |
| Capacitance | 4000 μF |

The current implementation uses the simplified relation

```
I = V / R
```

The coil inductance is currently assumed to be zero.

Future versions may include

- coil inductance,
- wiring resistance, and
- capacitor ESR

to implement a complete RLC transient model.

---

# 5. Solenoid Model

The solenoid force is based on the CB1037 datasheet.

The force is interpolated according to the striker position.

The resulting force is then scaled according to the actual current,

```
F(x,I)
```

Magnetic saturation is approximated using a

```
tanh()
```

function, preventing unrealistic force growth at high current.

---

# 6. Impact Model

The collision model uses

- conservation of momentum, and
- coefficient of restitution

to calculate

- ball launch speed, and
- ball angular velocity.

The restitution coefficient is currently an estimated value and should be calibrated experimentally.

---

# 7. Rolling Model

Ball motion is divided into

1. sliding,
2. pure rolling.

### Sliding

Uses

- sliding friction coefficient.

Calculates

- sliding time,
- sliding distance.

### Pure Rolling

Uses

- constant rolling deceleration.

Calculates

- rolling distance,
- stopping time.

---

# 8. Numerical Integration

Euler integration is currently used.

| Item | Value |
|------|-------|
| Time step | 0.01 ms |
| Height step | 0.1 mm |

These values can be modified in `config.py`.

---

# 9. Overall Calculation Procedure

1. Load configuration
2. Simulate capacitor discharge
3. Compute solenoid force
4. Integrate striker motion
5. Calculate impact
6. Simulate sliding
7. Simulate rolling
8. Export CSV

---

# 10. Current Assumptions

The following parameters are currently estimated.

| Parameter | Reason |
|-----------|--------|
| Coil inductance | No published data |
| Saturation knee current | No published data |
| Restitution coefficient | Not yet measured |
| Sliding friction coefficient | Not yet measured |
| Rolling deceleration | Not yet measured |

The sensitivity analysis tool can be used to determine which assumptions have the greatest influence on the simulation results.