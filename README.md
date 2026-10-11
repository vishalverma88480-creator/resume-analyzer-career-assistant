# Resume Analyzer & Career Assistant

A web-based application that analyzes resumes, calculates a resume-to-job skill match score, and provides career guidance and learning recommendations.

## Live Demo

- **Frontend:** https://resume-ai-analyzer-1-lzgp.onrender.com
- **Backend:** https://resume-analyzer-career-assistant.onrender.com

## Features

- Upload a resume in PDF format.
- Extract resume text and analyze skills.
- Calculate a skill-match score based on the required skills.
- Explore career paths and learning roadmaps.
- View previous resume analyses.
- Receive career and learning recommendations.
- Use a responsive interface designed for desktop and mobile screens.

## Tech Stack

**Frontend**
- React
- JavaScript
- HTML and CSS

**Backend**
- Python
- Flask
- PyPDF2
- REST API

**Database and Deployment**
- SQLite
- Git and GitHub
- Render

## How It Works

1. Upload a PDF resume.
2. The backend extracts readable text from the document.
3. The application identifies relevant skills and calculates a match score.
4. The results page displays the analysis and recommendations.
5. Users can explore career guidance and review previous analyses.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/vishalverma88480-creator/resume-analyzer-career-assistant.git
cd resume-analyzer-career-assistant
```

Set up the Python environment and install dependencies using the backend's requirements file:

```bash
cd backend
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend using the startup command configured for your Flask application.

For the frontend, open another terminal, navigate to the `frontend` folder, install the dependencies, and run the development server:

```bash
npm install
npm run dev
```

## Project Status

The frontend and backend are deployed on Render, and resume upload and analysis have been tested.

**Note:** Analysis history may not persist across service restarts if the deployed SQLite database is stored on Render's ephemeral filesystem.

## Author

Vishal Verma

GitHub: https://github.com/vishalverma88480-creator

LinkedIn: https://linkedin.com/in/vishal-verma-36b713260
