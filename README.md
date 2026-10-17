# COV-IA — Cognitive Optimization for AI Inference

**Experimental inference-policy simulator / Simulador experimental de políticas de inferencia**

COV-IA explores how a controller could adapt model size and numerical precision as simulated load changes. The current public repository is a **proof of concept**, not a benchmark of deployed model inference.

> **Evidence boundary:** Latency, accuracy and cost in `cov_ia.py` come from **predefined synthetic model profiles**, precision factors and randomly sampled synthetic workloads. The historical percentage improvements are **simulation outputs**, not independently measured improvements on real hardware, not validated financial savings and not clinical performance.

## What it contains / Qué incluye

| EN | ES |
| --- | --- |
| Four policies: Precision, Balanced, Performance, Ultra. | Cuatro políticas: Precision, Balanced, Performance y Ultra. |
| An experimental RG-inspired state controller with thresholds and cooldowns. | Un controlador de estado experimental inspirado en RG, con umbrales y tiempos de espera. |
| Simulated model-size/precision switching under changing workload. | Cambios simulados de modelo y precisión según la carga. |
| Printed comparisons of estimated latency, synthetic accuracy and relative cost. | Comparaciones de latencia estimada, precisión sintética y costo relativo. |

## Run the simulation / Ejecutar la simulación

Requires Python and NumPy; no GPU, API key or Ollama server is needed for the checked-in simulation.

```bash
python -m pip install numpy
python cov_ia.py
```

The program runs a baseline and four modes and prints a comparison. It samples randomness without a fixed seed; numeric outputs can vary between runs. It does not currently contain a demonstrated end-to-end Ollama inference benchmark.

## Reported sample / Ejemplo histórico

An earlier README listed approximately 33 ms (Precision), 32 ms (Balanced/Performance) and 19 ms (Ultra), with relative cost reductions in the synthetic comparison. These are **illustrative outputs only**. Run the script to obtain results for your execution; do not interpret the table as hardware measurements or deployable performance guarantees.

## Repository map / Archivos

- [`cov_ia.py`](cov_ia.py) — simulation, policies and report output.
- [`cov_config.json`](cov_config.json) — separate experimental configuration.
- [`cov_rules_stray.json`](cov_rules_stray.json) — experimental visual-quality rules; not integrated into the inference simulation.
- [`cov_state.json`](cov_state.json) — saved experimental state.

**Research context / Contexto:** The RG-inspired controller is motivated by the author's TCF research ideas. Its relationship to physical theories and its usefulness for real inference optimization remain research questions, not externally validated results.

**Next validation / Próxima validación:** fixed-seed regression tests, explicit baseline comparison, real provider/hardware latency and token cost measurements, independent quality evaluation, and reproducible datasets.
