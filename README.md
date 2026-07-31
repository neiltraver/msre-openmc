# MSRE Temperature Coefficient of Reactivity Study

A CAD-based Monte Carlo neutron transport study of the Molten Salt Reactor Experiment (MSRE), built with [OpenMC](https://openmc.org) and DAGMC. The goal of this project is to measure the MSRE's **temperature coefficient of reactivity** — the passive safety feedback that made the reactor self-stabilizing — and compare the result against historical measurements from Oak Ridge National Laboratory.

## Attribution

This project builds on the MSRE CAD model developed by **Copenhagen Atomics / the openmsr project**, and follows the OpenMC/DAGMC workflow demonstrated in their tutorial:

- CAD model source: [openmsr/msre](https://github.com/openmsr/msre) (GPL-3.0)
- Tutorial video: [OpenMC Tutorial | Converting the World's Most Detailed MSRE CAD Model to Simulation](https://www.youtube.com/watch?v=ACPehDVfUrE)

The base geometry (CAD `.step` files), material definitions, and the initial criticality script follow that tutorial. Everything from the temperature coefficient study onward — temperature-dependent salt density coupling, the reactivity sweep, and the analysis — is my own extension.

## Background

A reactor's temperature coefficient of reactivity, α = Δρ/ΔT, describes how reactivity responds to a change in temperature. A **negative** coefficient means that heating the core reduces reactivity, so power excursions are self-limiting: rising power → rising temperature → falling reactivity → falling power. The MSRE was designed to exhibit strongly negative feedback through two mechanisms:

1. **Doppler broadening** — higher fuel temperature broadens absorption resonances, increasing parasitic neutron capture.
2. **Fuel salt thermal expansion** — because the fuel is a liquid, heating reduces its density and pushes fissile material out of the core region.

This study models both effects by coupling the fuel salt's temperature and density to a single parameter and sweeping it across a range of temperatures.

## Model

- **Geometry:** CAD-based (DAGMC) model of the MSRE core, reactor pit, and control rod, converted from `.step` files to `.h5m` surface meshes.
- **Materials:** LiF-BeF₂-ZrF₄-UF₄ fuel salt, graphite moderator, INOR-8 vessel, Inconel-600 and SS316 structural components, at component-appropriate temperatures.
- **Nuclear data:** ENDF/B-VIII.0, with temperature interpolation enabled.
- **Salt density:** temperature-dependent, using the ORNL-3913 experimental correlation:

  ρ (g/cm³) = 2.848 − 7.693×10⁻⁴ · T (°C)

- **Code:** OpenMC 0.14.0, k-eigenvalue mode.

## Method

1. Set the fuel salt temperature `salt_temp` (°C). Salt, graphite, and vessel temperatures and the salt density update from this single parameter.
2. Run the k-eigenvalue simulation and record combined k-effective and its uncertainty.
3. Convert to reactivity: ρ = (k − 1)/k.
4. Repeat across a range of salt temperatures.
5. Fit reactivity vs. temperature; the slope is the temperature coefficient α.

## Results

Study in progress — results will be added as the temperature sweep is completed.

## Repository contents

| File | Description |
|---|---|
| `msre_critical.py` | Main OpenMC model and k-eigenvalue run script |
| `step_to_h5m.py` | Converts CAD `.step` files to DAGMC `.h5m` meshes |
| `*.step` | MSRE CAD geometry, from [openmsr/msre](https://github.com/openmsr/msre) (GPL-3.0) |

Large generated files (`.h5m` meshes, statepoint and summary files) are not tracked and can be regenerated from the scripts.

## Reproducing

```bash
micromamba activate <env-with-openmc-and-dagmc>
python step_to_h5m.py      # regenerate .h5m geometry from .step files
python msre_critical.py    # run the simulation
```

Requires OpenMC 0.14.0 with DAGMC support and the ENDF/B-VIII.0 HDF5 data library (`OPENMC_CROSS_SECTIONS` must point to its `cross_sections.xml`).

## References

- ORNL-3913, *Reactor Chemistry Division Annual Progress Report* — source of the MSRE fuel salt density correlation.
- openmsr/msre repository documentation and linked MSRE design reports.
- P. K. Romano et al., "OpenMC: A state-of-the-art Monte Carlo code for research and development," *Ann. Nucl. Energy* 82 (2015).

## License

This repository is licensed under the **GNU General Public License v3.0**, consistent with the upstream MSRE CAD model from [openmsr/msre](https://github.com/openmsr/msre). The CAD geometry remains the work of Copenhagen Atomics / the openmsr project; my scripts and analysis are released under the same terms.


