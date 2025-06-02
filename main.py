from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI(
    title="ChemGPT Spectroscopy Microservice",
    description="Handles all spectroscopy-related tasks for ChemGPT (UV, IR, etc.)",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "chemgpt-spectro", "message": "Spectroscopy microservice is alive!"}

class MoleculeRequest(BaseModel):
    molecule: str

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set!")

@app.post("/spectroscopy")
async def spectroscopy_endpoint(data: MoleculeRequest):
    molecule = data.molecule.strip()
    if not molecule:
        raise HTTPException(status_code=400, detail="Molecule name or SMILES required.")

    # Build GPT-4o prompt for spectra
    prompt = (
    f"You are a world-class chemistry assistant and spectral database. "
    f"For the molecule '{molecule}', provide the following as comprehensively as possible, using markdown: \n\n"
    "1. **Infrared (IR) Spectrum Table**: For each main peak, give: wavenumber (cm⁻¹), intensity, assignment (functional group or bond type), and a brief note if relevant. "
    "Add as many peaks as possible from known literature/experimental data.\n\n"
    "2. **UV-Visible (UV-Vis) Spectrum Table**: For each peak, give: wavelength (nm), intensity, transition type (e.g., π→π*, n→π*), and a note if available. "
    "List all significant peaks.\n\n"
    "3. **NMR Spectra Tables (¹H and ¹³C)**: For each, give: chemical shift (δ, ppm), multiplicity (s, d, t, q, m), coupling constant (J, Hz) if known, assignment (proton or carbon type), and integration if possible. "
    "Add all signals typically observed for this molecule.\n\n"
    "4. **Summary of Key Features**: Briefly interpret the spectra—mention characteristic signals or peaks, functional groups identified, and what a chemist can deduce.\n\n"
    "5. **References**: If possible, cite databases or literature sources (e.g., NIST, SDBS, PubChem, Spectral Database for Organic Compounds).\n\n"
    "Return only markdown tables (one for each spectrum), and summary/reference sections as bullet points. "
    "Be as complete and accurate as possible, but if data is missing for any part, clearly state 'Not available'."
)

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=700
        )
        answer = response.choices[0].message.content
        return {
            "molecule": molecule,
            "spectra_markdown": answer,
            "source": "AI-generated spectra via GPT-4o"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
