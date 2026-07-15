# Vaccine Distribution Contracts

> An Algorand smart contract for tracking vaccine inventory across distribution stores, built with Beaker and PyTeal.

## Overview

`vaccine-contracts` is a stateful Algorand application named **VaccineDistribution**. It models a simple vaccine supply-chain registry: a network-wide admin, a count of distribution stores and available vaccines, per-account roles, and a per-store inventory kept in box storage. The contract is written in Python using the [Beaker](https://algorand-devrel.github.io/beaker/html/index.html) framework on top of PyTeal, and it ships with a deploy/exercise script that runs against a local Algorand sandbox.

This is a compact, hands-on project exploring Algorand global state, local (per-account) state, and box storage rather than a production-ready system.

## Features

- **Global registry state** — tracks `TotalVaccines`, `TotalStores`, and `GlobalVaccineAvailability` as on-chain global state values.
- **Admin address** — stores an `AdminAddress` that can be set and read via contract methods.
- **Static app version** — an immutable `AppVersion` global value (`1.0.0`) demonstrating static state.
- **Per-account roles** — local state `Role` (default `"User"`) set and read against the transaction sender, with automatic opt-in on account registration.
- **Per-store inventory in boxes** — a `BoxMapping(String → String)` (`inventory`) that stores each store's vaccine data as a JSON string, written via `set_vaccine_quantity` and read back via `readItem`.
- **Prebuilt artifacts** — compiled `approval.teal`, `clear.teal`, and the ABI/application JSON are included under `artifacts/`.

## Tech Stack

- **Python** — contract and tooling language
- **Beaker** — Algorand smart contract framework
- **PyTeal** — TEAL generation
- **algokit-utils** — deployment and logic-error handling
- **Algorand Sandbox / LocalNet** — local deployment target (via Beaker `sandbox`)

## Getting Started

Requires Python 3 and a running Algorand LocalNet (for example via [AlgoKit](https://developer.algorand.org/docs/get-started/algokit/)).

```bash
# Install dependencies
pip install beaker-pyteal algokit-utils

# Start a local Algorand network (AlgoKit)
algokit localnet start

# Build the contract artifacts and deploy + exercise it on the sandbox
python deploy.py
```

`deploy.py` builds the app, exports artifacts to `./artifacts`, creates and funds the application, then calls the contract methods to set and read global state, roles, and store inventory.

## Project Structure

```
.
├── vaccine.py        # VaccineDistribution contract: state, roles, box-based inventory
├── deploy.py         # Build, deploy to sandbox, and exercise the contract methods
├── test.py           # JSON encode/decode scratch script
└── artifacts/        # Compiled output
    ├── approval.teal
    ├── clear.teal
    ├── application.json
    └── contract.json  # ABI definition
```

---

Built by [nickthelegend](https://github.com/nickthelegend) · [nickthelegend.tech](https://nickthelegend.tech)
