# DEC-02: Simulation

**Status:** Accepted
**Date:** 2026-10-10
**Decision owner:** Integration repository maintainer
**Due date:** 2026-10-10 (completed)
**Domain review:** Approved for the bounded demonstration by the sole cross-project maintainer on 2026-10-10; no independent domain reviewer was available

## Context

The shared contract kit needs one deterministic simulation whose results can be
reproduced in different implementation languages. It is a bounded integration
demonstration, not a certified engineering calculation.

## Decision

### PV and inverter

- The simulation uses one-hour intervals.
- Hourly DC generation is the selected PV capacity in `kWp` multiplied by the
  `PV_YIELD_PER_KWP` value for that interval.
- Inverter efficiency is applied before enforcing the inverter AC power limit.
  For a one-hour interval:

  ```text
  pvDcKWh = installedPvKWp * pvYieldKWhPerKWp
  pvAcKWh = min(pvDcKWh * inverterEfficiency, inverterAcPowerKW * 1 h)
  ```

- The difference between efficiency-adjusted potential output and the inverter
  limit is recorded as inverter clipping.

### Battery dispatch

- PV serves the building load first.
- Remaining PV charges the battery within its usable-capacity and charge-power
  limits. Remaining surplus is exported.
- When PV is insufficient, the battery discharges within its state-of-charge
  and discharge-power limits. Remaining demand is imported.
- Grid charging and simultaneous charging and discharging are prohibited.
- Charge and discharge efficiencies are each the square root of the recorded
  round-trip efficiency.
- Battery charge and discharge power limits are AC-side limits. For a one-hour
  interval, state of charge changes by:

  ```text
  nextSocKWh = socKWh
             + chargeAcKWh * chargeEfficiency
             - dischargeAcKWh / dischargeEfficiency
  ```

- State of charge starts at zero. Any residual state of charge after the final
  interval is recorded as `terminalDiscardedEnergyKWh`, receives no cost or
  self-sufficiency credit, and is discarded so the modeled year ends at zero.

### Economics

- The first release uses a 20-year analysis period and a `0.04` annual discount
  rate.
- Every component has a modeled economic lifetime of 20 years.
- Component replacement, residual value, maintenance, installation labor,
  taxes, and subsidies are excluded.
- Annual operations cost is zero.
- Initial investment is the sum of unit price multiplied by newly purchased
  component quantity. Existing equipment is excluded from initial investment.
- Initial investment is annualized with the capital-recovery-factor formula in
  the integration contract.

### Numeric behavior

- Implementations use IEEE-754 binary64 calculations and do not round
  intermediate hourly values.
- Energy outputs are serialized to six decimal places and monetary outputs to
  two decimal places using round-half-to-even.
- Ranking uses annualized cost rounded to cents, then initial investment rounded
  to cents, then lexical configuration ID.
- The energy-balance tolerance is an absolute `1e-6 kWh` per hourly interval.
- Dimensionless comparisons, including self-sufficiency, use an absolute
  tolerance of `1e-9`.
- Contract tests compare serialized monetary values exactly and serialized
  energy values within `1e-6 kWh`.

## Consequences

- Battery behavior is deterministic and designed to maximize direct use of PV;
  it does not perform price arbitrage or forecast-aware dispatch.
- Discarding terminal battery energy is an explicit boundary treatment. It must
  appear in evidence and energy-balance tests rather than being hidden as a
  numerical loss.
- The simplified lifetime and cost model must be disclosed to users. More
  realistic replacements, degradation, maintenance, or residual values require
  a new simulation version and updated expected results.
- This baseline has maintainer review but no independent review by a certified
  energy engineer. It cannot support certified or production engineering claims.
- The shared contract kit must contain hand-calculated cases for PV clipping,
  charge and discharge efficiency, capacity and power limits, import, export,
  terminal discarded energy, and all numeric tolerances.
