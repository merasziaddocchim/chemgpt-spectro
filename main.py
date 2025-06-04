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
    f"You are ChemGPT, the world’s most advanced AI chemistry spectral assistant—like a Nobel laureate, database, and educator in one. "
    f"Your task: For the molecule '{molecule}', generate a complete and highly structured spectral analysis. "
    "Be as comprehensive, accurate, and educational as possible, drawing on authoritative sources, but clearly state if any info is unavailable or uncertain.\n\n"

    "Organize your answer in these clearly labeled sections:\n\n"

    "## 1. Infrared (IR) Spectrum Table\n"
    "- For each **main peak**, include: wavenumber (cm⁻¹), intensity (strong, medium, weak, broad, sharp), assignment (functional group or bond type), and a brief annotation or caveat if relevant.\n"
    "- Include as many peaks as are typically reported in reputable literature or spectral databases.\n"

    "## 2. UV-Visible (UV-Vis) Spectrum Table\n"
    "- For each significant **peak**, provide: wavelength (nm), intensity, transition type (e.g., π→π*, n→π*), molar absorptivity (if known), and a short note (e.g., chromophore type, solvent used).\n"

    "## 3. NMR Spectra Tables\n"
    "- ### ¹H NMR Table:\n"
    "  - For each unique signal, list: chemical shift (δ, ppm), multiplicity (s, d, t, q, m, etc.), coupling constant (J, Hz, if known), integration, assignment (proton environment/type), and any special notes.\n"
    "- ### ¹³C NMR Table:\n"
    "  - For each signal, give: chemical shift (δ, ppm), assignment (carbon type/environment), and any relevant comments (e.g., quaternary carbon, symmetry).\n"

    "## 4. Summary of Key Spectral Features\n"
    "- Briefly interpret and connect the main features from all spectra (IR, UV, NMR): "
    "  - Highlight diagnostic peaks, confirmatory signals, unusual findings, and functional groups. "
    "  - Clearly explain what a chemist can deduce about the structure and purity from the spectra.\n"

    "## 5. References\n"
    "- List all database sources (e.g., NIST, SDBS, PubChem, SDBS Japan), textbooks, or literature citations used to construct the answer. "
    "- For well-known molecules, include links or DOIs if possible.\n"

    "## 6. Data Availability & Confidence\n"
    "- For each section, if data is missing, ambiguous, or varies in the literature, explicitly say so. "
    "State your confidence level for each spectrum (e.g., 'IR: High confidence based on NIST entry X; ¹³C NMR: Moderate, some shifts estimated').\n"

    "## 7. Visualization Table Block\n"
    "- For each spectrum (IR, UV, ¹H NMR, ¹³C NMR), output a **machine-readable table** as markdown, using columns for the main values (e.g., wavenumber, intensity, assignment), suitable for parsing and frontend plotting.\n"

    "## 8. 'You might also ask:'\n"
    "- Suggest 2–3 related questions a chemist or student might ask next, e.g., about spectra for related molecules, how to interpret challenging peaks, or about experimental setup.\n"

    "⚠️ Use bullet points, numbered lists, and clean markdown tables. Label every section clearly. "
    "Never invent data; state 'Not available' if uncertain or missing. "
    "Be maximally helpful for students, researchers, and chemists. "
    "Never give just dense text—always structure output for both human readability and frontend parsing/visualization."
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
