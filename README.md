# PolyGen

**A planned text-to-3D asset pipeline for games, VR, and spatial computing.**

PolyGen is intended to turn natural-language descriptions into 3D assets that can be previewed and exported. This repository now contains a small frontend and FastAPI scaffold; AI model generation, texturing, mesh optimization, 3D viewing, and export are not implemented yet.

## Current functionality

- The frontend development server displays a scaffold landing page.
- `GET /` and `GET /health` provide basic backend status responses.
- `POST /api/generate` validates a prompt (3-500 characters) and returns a `pending` placeholder response. It does not generate a model.

## Project structure

```text
PolyGen/
├── frontend/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── viewer/
│       ├── App.jsx
│       ├── index.css
│       └── main.jsx
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── optimization/
│   │   ├── routes/
│   │   ├── services/
│   │   └── texture/
│   ├── main.py
│   └── requirements.txt
├── documentation/
├── generated_models/
└── README.md
```

## Requirements

- Node.js and npm
- Python 3.10 or newer

## Run locally

Start the backend from the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

On Linux or macOS, activate the virtual environment with:

```bash
source .venv/bin/activate
```

In a second terminal, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (normally `http://localhost:5173`). The backend API is available at `http://localhost:8000`; interactive API documentation is at `http://localhost:8000/docs`.

## API

### `GET /`

Returns the project name and backend status.

### `GET /health`

Returns `{"status":"healthy"}`.

### `POST /api/generate`

Request:

```json
{
  "prompt": "A small stone lantern"
}
```

The prompt must contain between 3 and 500 characters. The response indicates that generation is pending; no 3D asset is produced at this stage.

## Planned pipeline

1. Accept and enhance a text prompt.
2. Generate a 3D model.
3. Generate and apply textures and UV mapping.
4. Clean and optimize the mesh.
5. Preview the model interactively.
6. Export as GLB or glTF.

Proposed future technologies include React, Vite, Three.js / React Three Fiber, FastAPI, TripoSR or Shap-E, Stable Diffusion / ControlNet, trimesh, and Open3D. These AI and 3D processing integrations are not part of the current scaffold.
