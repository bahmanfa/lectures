# Regime Signal Analysis - Validation Audit Report

Generated: 2026-07-08T16:26:47  
Pipeline version: **6.0.0**  
Runtime mode: **research**  

> **STATUS: PASSED**

## Run context

| Field | Value |
|---|---|
| manifest_hash | 3099e7eaca46de22... |
| config_hash | None |
| regime_file_hash | None |
| returns_file_hash | None |
| script_source_hash | 296adb74ec495ff1... |
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

- Total checks: **15**
- Passed: **15**
- Warnings: **0**
- Failures: **0**

| Check | Status | Detail |
|---|---|---|
| cache_manifest | PASS | {'manifest_hash': '3099e7eaca46de225138d3c946dfa1e3a10abceddc9ecd26b73b3d4adf02d882', 'matched_prev': False} |
| config_validation | PASS | {'mode': 'research', 'subset_n_run_ids': None} |
| date_validation_regime | PASS | {'col': 'date_eom', 'n_invalid': 0} |
| date_validation_returns | PASS | {'col': 'date', 'n_invalid': 0} |
| duplicate_policy | PASS | {'duplicate_policy': 'drop', 'dedupe_key_used': 'idstate2,next_h_ym,idmethod,horizon,source_date_eom', 'n_before': 17... |
| headline_p_method_check | PASS | adjusted_min_p |
| idmethod_dtype | PASS | string |
| k_effective | PASS | {'k_eff': 1.0, 'k_raw': 1} |
| k_effective_method_check | PASS | corrected_li_ji |
| panel_cardinality | PASS | {'grain': ['idmethod', 'date_eom']} |
| reg_slim_panel | PASS | {'grain': ['run_id', 'date_eom']} |
| regime_cardinality | PASS | {'grain': 'idmethod+date_eom', 'duplicate_groups': 0} |
| regime_schema | PASS | ['date_eom', 'idmethod', 'idstate'] |
| returns_cardinality | PASS | {'grain': ['asset_class', 'asset_name', 'return_type', 'year_month'], 'duplicate_rows': 0} |
| subsample_stability | PASS | {'overall_pass_frac': 0.24444444444444444} |


## Unit tests (production-hardening contract)

8/8 tests passed.

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
