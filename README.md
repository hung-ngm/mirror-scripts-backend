# MirrorScripts Backend

Backend for MirrorScripts - An app that helps create research reports automatically with references using AI

## How to run:

1. Clone the repository
2. Navigate to the backend directory: `cd mirror_scripts_agent`
3. Create virtual environment and install packages:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
4. Run the local backend:
   ```bash
   uvicorn main:app --reload
   ```