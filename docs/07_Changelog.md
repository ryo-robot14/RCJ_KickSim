# RCJ_KickSim Changelog

All notable changes to this project are documented in this file.

The format is based on **Keep a Changelog** and follows **Semantic Versioning**.

---

## [Unreleased]

### Added

- `config.py` を追加し、ユーザー設定とシミュレーション本体を分離
- `main.py` による高さスイープ機能
- `plot_sweep.py` によるターミナルグラフ表示
- `analyze_trials.py` による実測データ解析
- `sensitivity.py` によるモンテカルロ感度解析
- コンデンサ放電（RC）モデル
- ソレノイド推力モデル（CB1037データシート対応）
- ストライカー運動モデル
- ボール衝突モデル
- スリップ・転がりモデル
- CSVレポート出力
- ドキュメント体系を整備
  - README
  - 01_ProjectPlan
  - 02_UserGuide
  - 03_PhysicsModel
  - 04_Configuration
  - 05_DeveloperGuide
  - 06_Validation
  - 07_Changelog

### Changed

- `constants.py` を `config.py` を利用する構成へリファクタリング
- プロジェクト全体をモジュール構造へ整理
- シミュレーションパイプラインを整理・再構成
- README を日本語・英語併記へ更新
- ドキュメント全体を日本語・英語併記へ更新
- コードコメントおよびDocstringを整理

### Fixed

- 長時間シミュレーション時の無限ループ防止
- 高さ探索時のCSV出力処理を改善
- パラメータ管理の重複を解消

---

## [0.1.0] - 2026-07

### Added

- プロジェクト開始
- GitHub リポジトリ作成
- 基本ディレクトリ構成
- 初期シミュレーションコード

---

## [Unreleased]

### Added

- Added `config.py` to separate user configuration from the simulator implementation
- Kick-height sweep using `main.py`
- Terminal plotting with `plot_sweep.py`
- Experimental-data analysis with `analyze_trials.py`
- Monte Carlo sensitivity analysis with `sensitivity.py`
- RC capacitor-discharge model
- CB1037 solenoid force model
- Striker dynamics model
- Ball impact model
- Sliding and rolling model
- CSV reporting
- Complete project documentation
  - README
  - 01_ProjectPlan
  - 02_UserGuide
  - 03_PhysicsModel
  - 04_Configuration
  - 05_DeveloperGuide
  - 06_Validation
  - 07_Changelog

### Changed

- Refactored `constants.py` to load parameters from `config.py`
- Reorganized the project into a modular architecture
- Refined the simulation pipeline
- Updated the README to bilingual (Japanese/English)
- Updated all documentation to bilingual (Japanese/English)
- Improved code comments and docstrings

### Fixed

- Prevented potential infinite loops during long simulations
- Improved CSV generation during kick-height sweeps
- Removed duplicated parameter definitions

---

## [0.1.0] - 2026-07

### Added

- Initial project setup
- GitHub repository
- Base directory structure
- Initial simulation implementation