# Hybrid_KAVe

This repository contains an interactive runner to execute Hybrid KAVe experiments on:

- **Snippets** (the curated vulnerable/safe samples under `Samples/`)
- **Web apps** (the PHP web app projects under `WebAppSample/`)

The main entrypoint for day-to-day usage is **`run_experiment.py`**.

## Quick Start

Use Python 3.10+ (Windows tested). You can run this project **without** creating a virtual environment.

### Option A (no venv): Install dependencies globally and run

This is the simplest path for a quick test.

Windows (PowerShell), from the repository root:

- `python -m pip install -U pip`
- `python -m pip install networkx openai`
- `python run_experiment.py`

Linux (bash), from the repository root:

- `python3 -m pip install -U pip`
- `python3 -m pip install networkx openai`
- `python3 run_experiment.py`

Notes:

- If you don’t want GPT-assisted mode, you can omit `openai`.

### Option B (recommended): Use a virtual environment

This avoids dependency conflicts and makes runs more reproducible.

Windows (PowerShell):

- `python -m venv .venv`
- `.\\.venv\\Scripts\\Activate.ps1`
- `python -m pip install -U pip`
- `python -m pip install networkx openai`
- `python run_experiment.py`

Linux (bash):

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install -U pip`
- `python -m pip install networkx openai`
- `python run_experiment.py`

### Dependencies

This project relies on a few Python packages. At minimum you will typically need:

- `networkx`
- `openai` (only if you want GPT-assisted mode)

Install:

- `pip install -U pip`
- `pip install networkx openai`

If you run into missing-package errors, install what the error message reports.

### 3) Run the interactive runner

From the repository root:

- `python run_experiment.py`

You will see a menu:

- **Run on Snippets** (runs scripts from `Scripts/`)
- **Run on Web Apps** (runs the KAVe analysis via `SAT/main.py`)

## Using `run_experiment.py`

### Mode A: Run on Snippets

1. Start the runner: `python run_experiment.py`
2. Choose: `1` **Run on Snippets**
3. Pick a script from `Scripts/` (e.g., `rungpt_kave.py`, `rungemini_kave.py`, etc.)

Notes:

- The snippet scripts typically analyze the predefined sample folders.
- Depending on the selected script, the runner will prompt for the required API key and set it **only for that run**:
	- GPT scripts: `OPENAI_API_KEY`
	- Gemini scripts: `GOOGLE_API_KEY` / `GEMINI_API_KEY`
	- DeepSeek scripts: `DEEPSEEK_API_KEY`
- Outputs are saved under `output/` with a timestamp.

### Mode B: Run on Web Apps (KAVe Analysis)

1. Start the runner: `python run_experiment.py`
2. Choose: `2` **Run on Web Apps**
3. Choose analysis mode:
	 - `1` Simple KAVe (no GPT)
	 - `2` KAVe with GPT assistance
4. Select a target under `WebAppSample/` (e.g., `Folder: currentcost`)

The runner executes the SAT analyzer:

- `SAT/main.py <web_app_path>`

and writes a timestamped log file to `output/`.

## GPT-Assisted Mode

If you select **KAVe with GPT assistance**, the runner will prompt you for an API key.

- Paste your key at the prompt (it will set `OPENAI_API_KEY` only for that run)
- Or press Enter to skip (GPT will not run)

## Outputs

`run_experiment.py` writes logs into:

- `output/`

For example:

- `output/webapp_kave_simple_YYYYMMDD_HHMMSS.txt`
- `output/webapp_kave_gpt_YYYYMMDD_HHMMSS.txt`

Some SAT components may also write additional artifacts under:

- `SAT/AI_results/`

## Troubleshooting

### “GPT mode runs but looks identical to non-GPT”

Common causes:

- `OPENAI_API_KEY` wasn’t provided (or is invalid)
- The `openai` package is not installed in the Python environment you used to run

Fix:

- Ensure you installed deps in the same environment: `pip install openai`
- Re-run and paste your API key when prompted

### PowerShell execution policy (Windows)

If activating the venv fails due to execution policy:

- `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Graphviz / pygraphviz errors

Some optional graph-drawing functionality may require Graphviz/pygraphviz.
If you encounter those errors and you don’t need graph visualization, you can ignore
the drawing features (the analysis itself does not require graph rendering).

## Reproducibility tip

If you want consistent results across machines, always run from the repo root and
use the same Python environment (e.g., `.venv`).