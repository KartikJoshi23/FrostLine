"""The audited chain numbers (audit of 24 November 2026; plan 1.4, 2.2, 2.7, 5.5).

Counted to the end of 23 November 2026 (UTC). The registry must reproduce every one
of them before anything is built on it (plan 2.2, acceptance checks).
"""

from datetime import UTC, datetime

AUDIT_CUT = int(datetime(2026, 11, 24, tzinfo=UTC).timestamp() * 1000)

AUDIT_NUMBERS = {
    "freeze_release_destroy_events": [9357, 1007, 1309],
    "ever_frozen": 9317,
    "still_frozen_at_cut": 8324,
    "to_12_aug_2026_events_and_wallets_incl_contract": [8017, 7987],  # Bitquery
    "on_8_nov_2026_still_and_ever": [8206, 9191],  # FreezeCheck
    "ever_released_wallets": 1007,
    "destroyed_wallets": 1265,
    "frozen_more_than_once": 36,
    "first_freezes_by_year": {
        "2020": 13,
        "2021": 21,
        "2022": 311,
        "2023": 271,
        "2024": 1223,
        "2025": 3506,
        "2026": 3972,
    },
    "released_14_may_2026": 447,
    "freezes_matched_to_votes": 9328,
    "unmatched_by_year": {"2020": 14, "2021": 15},
    "negative_gaps": 0,
    "freeze_time_batches": 1508,
    "batch_median_gap_minutes": 68.2,
    "batch_median_gap_2024_25": 103.1,
    "batch_median_gap_2026": 23.2,
    "share_batches_over_1h": 52.0,
    "wallets_in_freeze_batches_5plus_pct": 78.3,
    "largest_freeze_batch": [779, "2025-07-12"],
    "freezecheck_window_events": 4221,  # FreezeCheck's window
    "wallets_with_executed_vote": 9292,
    "wallets_in_vote_batches_5plus_pct": 73.3,
    "unexecuted_submissions": 134,
    "unexecuted_freeze_votes": 95,
    "their_targets_never_frozen": 44,
    "wallets_with_earlier_unexecuted_vote": 18,
    "max_earlier_vote_days": 34,
}

# Split counts with the audit's definition: S = first executed vote; batches counted per split.
AUDIT_SPLITS = {
    "description": {
        "wallets": 1046,
        "batches": 284,
        "released": 117,
        "destroyed": 399,
        "largest_batch": 114,
    },
    "learn": {
        "wallets": 3701,
        "batches": 591,
        "released": 197,
        "destroyed": 517,
        "largest_batch": 779,
    },
    "tune": {"wallets": 573, "batches": 137, "released": 46, "destroyed": 167, "largest_batch": 36},
    "test": {
        "wallets": 3794,
        "batches": 759,
        "released": 643,
        "destroyed": 163,
        "largest_batch": 173,
    },
    "held_out": {"wallets": 178, "batches": 58, "released": 0, "destroyed": 0, "largest_batch": 17},
}
