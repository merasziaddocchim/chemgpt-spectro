# chemgpt-spectro

# chemgpt-spectro

**Spectroscopy microservice for ChemGPT.**

- FastAPI + Docker + Railway-ready
- Handles all UV/IR/NMR/molecular spectra endpoints
- Can be deployed 100% cloud, no local dependencies

## Endpoints

- `/` – Health check
- `/spectroscopy` – POST: Generate/return spectra for molecules
