# Regime Signal Analysis - Validation Audit Report

Generated: 2026-07-08T17:11:11  
Pipeline version: **6.1.0**  
Runtime mode: **research**  

> **STATUS: PASSED**

## Run context

| Field | Value |
|---|---|
| manifest_hash | 370b79e6b89e60c0... |
| config_hash | None |
| regime_file_hash | None |
| returns_file_hash | None |
| script_source_hash | d8bd2cd2d6bad87d... |
| headline_p_method | adjusted_min_p |
| k_effective_method | corrected_li_ji |
| min_occurrences | 12 |
| duplicate_policy | drop |
| k_eff | 1.0 |
| k_naive | 1 |
| n_run_ids | 4 |
| n_shards | 4 |
| n_cells | 180 |
| subsample_overall_pass | 0.24444444444444444 |

## State-fill policy

- **use_ffilled_date_as_coverage_end_date**: True
- **allow_post_coverage_ffill**: False
- **max_ffill_months**: 24
- **mark_stale_after_months**: 6

## Validation checks

- Total checks: **17**
- Passed: **17**
- Warnings: **0**
- Failures: **0**

| Check | Status | Detail |
|---|---|---|
| cache_manifest | PASS | {'manifest_hash': '370b79e6b89e60c0f4872972569f17c5c5f0f750d16577847f4b460b7d92eaf6', 'matched_prev': False} |
| config_validation | PASS | {'mode': 'research', 'subset_n_run_ids': None} |
| date_validation_regime | PASS | {'col': 'date_eom', 'n_invalid': 0} |
| date_validation_returns | PASS | {'col': 'date', 'n_invalid': 0} |
| duplicate_policy | PASS | {'duplicate_policy': 'drop', 'dedupe_key_used': 'idstate2,next_h_ym,idmethod,horizon,source_date_eom', 'n_before': 17... |
| headline_method_agreement | PASS | {'agreement_rate': 0.5, 'n_disagree': 2, 'n': 4} |
| headline_p_method_check | PASS | adjusted_min_p |
| idmethod_dtype | PASS | string |
| k_effective | PASS | {'k_eff': 1.0, 'k_raw': 1} |
| k_effective_method_check | PASS | corrected_li_ji |
| panel_cardinality | PASS | {'grain': ['idmethod', 'date_eom']} |
| reg_slim_panel | PASS | {'grain': ['run_id', 'date_eom']} |
| regime_cardinality | PASS | {'grain': 'idmethod+date_eom', 'duplicate_groups': 0} |
| regime_schema | PASS | ['date_eom', 'idmethod', 'idstate'] |
| returns_cardinality | PASS | {'grain': ['asset_class', 'asset_name', 'return_type', 'year_month'], 'duplicate_rows': 0} |
| sensitivity_report | PASS | {'n_rows': 12, 'path': '/tmp/regv6_e2e_tv_ca4wj/outputs/sensitivity_report.csv'} |
| subsample_stability | PASS | {'overall_pass_frac': 0.24444444444444444} |

## Headline-method agreement

Agreement between the two dependence-robust headline combiners (Cauchy combination vs adjusted-min-p / Sidak) on the significant / not-significant call. High agreement strengthens the inference; disagreements flag configs with unusual dependence structure.

- Alpha: **0.05**
- Agreement rate: **50.0%** (2/4 agree, 2 disagree)
- Disagreeing run_ids (up to 25): fwdfill|imid101, fwdfill|imidmethod_foo

## Sensitivity report

How the significant-config / significant-cell counts move as four robustness axes are varied. Stability across all axes is evidence of a robust regime-asset relationship; collapse under any single axis surfaces fragility. See `sensitivity_report.csv` for the machine-readable version.

| Axis | Setting | Sig. configs | Sig. cells (BH) | Baseline | Note |
|---|---|---|---|---|---|
| headline_p_method | adjusted_min_p | 2.0 | nan | yes | free: pre-stored headline variant |
| headline_p_method | fisher_raw | 4.0 | nan |  | free: pre-stored headline variant |
| headline_p_method | cauchy_combination | 4.0 | nan |  | free: pre-stored headline variant |
| min_occurrences | 6 | nan | 52.0 |  | cell-level BH recount |
| min_occurrences | 12 | nan | 52.0 | yes | cell-level BH recount |
| min_occurrences | 18 | nan | 38.0 |  | cell-level BH recount |
| min_occurrences | 24 | nan | 38.0 |  | cell-level BH recount |
| k_effective_method | raw_k | nan | nan |  | k=1.000 |
| k_effective_method | corrected_li_ji | nan | nan | yes | k=1.000 |
| k_effective_method | galwey | nan | nan |  | k=1.000 |
| duplicate_policy | drop | 4.0 | nan | yes | executed policy |
| duplicate_policy | keep | nan | nan |  | counterfactual (see duplicate_policy_diagnostics.csv for grain impact) |


## Unit tests (production-hardening contract)

10/10 tests passed.

| Test | Issue | Status |
|---|---|---|
| test_1_forward_return_correctness | C1 | PASS |
| test_2_panel_cardinality | H2/H5 | PASS |
| test_3_resume_equivalence | C2/C3 | PASS |
| test_4_best_class_labeling | H1 | PASS |
| test_5_idmethod_dtype | H3 | PASS |
| test_6_k_eff_bounds | M1 | PASS |
| test_7_drop_keep_logic | sample spec | PASS |
| test_8_subsample_stability | stability spec | PASS |
| test_9_stability_calibration | stability spec | PASS |
| test_10_resume_equivalence_e2e | C2/C3 | PASS |
