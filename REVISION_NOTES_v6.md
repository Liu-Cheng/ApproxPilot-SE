# ApproxGuide v6 working draft

This version is the first manuscript draft aligned with the frozen final method definition verified against the DCT implementation.

## Frozen method facts used in the manuscript

- Title focus: **Closed-Loop DSE under Limited Synthesis Budgets**.
- Each configurable arithmetic site includes an **Exact** state (gene value 0) plus compatible approximate states.
- The chromosome therefore jointly determines approximation placement and unit binding.
- Fixed-exact nodes are not encoded in the chromosome.
- PPA surrogate: 5-model ensemble; ensemble mean is used by DSE.
- QoR/SSIM surrogate: updated together with the PPA surrogate after every real-evaluation round.
- Search engine: NSGA-III.
- High-fidelity acquisition: predicted nondominated sorting + crowding; no uncertainty/Hamming score in the final method.
- Final candidate identities are frozen before true PPA/QoR evaluation.

## Figure status

- `figures/measured_pareto.pdf` is intentionally retained from the previous draft **only for layout** because the user requested the old result figure for now.
- It must be regenerated before submission after all benchmark results are synchronized to the frozen final protocol.
- The framework figure is still a LaTeX placeholder. Replace it later with the manually redrawn PDF from PowerPoint.
- Closed-loop ablation and representative-design figures remain placeholders until manually drawn.

## Main writing changes from v5

- New title: `ApproxGuide: Closed-Loop DSE for Approximate Accelerators under Limited Synthesis Budgets`.
- Abstract rewritten around the limited-target-synthesis-budget problem rather than listing modules.
- Introduction rewritten as a continuous TCAD-style argument: expensive target evaluation -> limits of per-target data and transfer -> closed-loop budget use.
- Related Work contains prior work and the research gap only; it no longer explains ApproxGuide implementation.
- Methodology is the technical center of the paper: joint exact/approximate state formulation, unit-informed system PPA modeling, separate QoR modeling, closed-loop budget allocation, and true verification.
- Uncertainty/Hamming acquisition is explicitly excluded from the final method.
