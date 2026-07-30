# RCJ_KickSim Development Plan

---

## プロジェクト概要

RCJ_KickSim は、RoboCup Junior Soccer Open 用ソレノイドキッカーの設計を支援するための物理シミュレータです。

従来は試作と実験を繰り返してキッカーを設計していましたが、本プロジェクトでは物理シミュレーションを用いることで、試作回数を削減し、効率的に設計を最適化することを目的としています。

最終的には、実機と高い一致率を持つシミュレータを構築し、キック板高さや電源条件などの設計パラメータをシミュレーションによって最適化できることを目標としています。

---

## 開発ロードマップ

### Stage 1：開発環境の構築
- Python環境構築
- Git / GitHub管理
- プロジェクト構成の設計

### Stage 2：ソレノイド・ストライカー運動
- ソレノイド推力モデル
- コンデンサ放電モデル
- ストライカー運動解析

### Stage 3：ボールモデル
- ボール質量・慣性モーメント
- ボール初速度計算
- ボール回転速度計算

### Stage 4：衝突モデル
- ストライカーとボールの衝突
- 力積
- 反発係数
- 摩擦によるスピン生成

### Stage 5：転がりモデル
- 滑り運動
- 純転がりへの遷移
- 停止距離推定

### Stage 6：最適化
- キック板高さ探索
- 感度解析
- CSV出力

### Stage 7：実機検証
- 実測データとの比較
- パラメータ同定
- モデル精度向上

---

## 現在の進捗

### 実装済み

- ソレノイドモデル
- コンデンサ放電モデル
- ストライカー運動
- 衝突モデル
- 転がりモデル
- キック高さ探索
- CSV出力
- 感度解析

### 今後の予定

- CB1037の実測推力モデル
- コイルインダクタンス測定
- パラメータ自動最適化
- GUIの実装

---

## 最終目標

実機の挙動を高精度に再現できるシミュレータを構築し、実験回数を削減しながら効率的にソレノイドキッカーを設計できる環境を実現する。

---

## Project Overview

RCJ_KickSim is a physics-based simulator for designing and optimizing solenoid kickers used in RoboCup Junior Soccer Open robots.

Traditionally, kicker development relies on repeated prototyping and experimental testing. This project aims to reduce the number of physical prototypes by introducing a physics simulator capable of predicting kicker performance before manufacturing.

The final objective is to build a simulator that accurately reproduces real-world behaviour and enables optimization of design parameters such as kick-plate height and electrical conditions.

---

## Development Roadmap

### Stage 1: Development Environment
- Python project setup
- Git / GitHub management
- Project architecture

### Stage 2: Solenoid and Striker Dynamics
- Solenoid force model
- Capacitor-discharge model
- Striker motion

### Stage 3: Ball Model
- Ball mass and inertia
- Ball launch velocity
- Ball spin

### Stage 4: Impact Model
- Striker-ball collision
- Impulse calculation
- Restitution
- Spin generation due to friction

### Stage 5: Rolling Model
- Sliding motion
- Transition to pure rolling
- Rolling distance estimation

### Stage 6: Optimization
- Kick-height sweep
- Sensitivity analysis
- CSV export

### Stage 7: Experimental Validation
- Comparison with experimental data
- Parameter identification
- Model calibration

---

## Current Status

### Implemented

- Solenoid model
- Capacitor-discharge model
- Striker dynamics
- Ball impact
- Rolling model
- Kick-height optimization
- CSV export
- Sensitivity analysis

### Planned

- Measured CB1037 force model
- Coil inductance measurement
- Automatic parameter identification
- GUI

---

## Final Goal

Build a simulator that accurately reproduces the behaviour of a real RoboCup Junior Soccer Open kicker and enables efficient design optimization while reducing the number of physical prototypes required.