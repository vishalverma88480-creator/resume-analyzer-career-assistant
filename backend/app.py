
import os
import uuid
from datetime import datetime, timezone

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

from ats_checker import calculate_ats_score
from skill_extractor import extract_skills
from job_recommender import recommend_jobs
from roadmap import create_roadmap

from database import (
    create_table,
    save_analysis,
    get_history,
    get_analysis,
    delete_analysis
)


# --------------------------------------------------
# Flask application configuration
# --------------------------------------------------

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf"}

# Create the database table when the application starts.
create_table()


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def extract_pdf_text(filepath):
    """Extract readable text from every page of a PDF."""
    reader = PdfReader(filepath)
    extracted_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text.append(page_text)

    return "\n".join(extracted_text).strip()


def build_strengths(score, details, skills):
    """Identify strengths using predefined rules."""
    strengths = []

    section_data = details.get("sections", {})
    contact_data = details.get("contact", {})

    if len(section_data.get("found", [])) >= 4:
        strengths.append(
            "Most core resume sections were detected."
        )

    if score >= 70:
        strengths.append(
            "Your resume meets many of the predefined scoring criteria."
        )

    if details.get("action_verbs"):
        strengths.append(
            "Action-oriented language was detected."
        )

    if contact_data.get("email") and contact_data.get("phone"):
        strengths.append(
            "Email address and phone number were detected."
        )

    if len(skills) >= 5:
        strengths.append(
            "Several relevant technical skills were detected."
        )

    if not strengths:
        strengths.append(
            "Your resume has been analyzed. Review the improvement "
            "suggestions to identify your next steps."
        )

    return strengths


def build_improvements(score, details, skills):
    """Identify improvement areas using predefined rules."""
    improvements = []

    section_data = details.get("sections", {})
    contact_data = details.get("contact", {})

    required_sections = {
        "education",
        "experience",
        "skills",
        "projects",
        "contact"
    }

    found_sections = {
        section.lower()
        for section in section_data.get("found", [])
    }

    missing_sections = sorted(required_sections - found_sections)

    if missing_sections:
        improvements.append(
            "Review these sections and add any that are relevant: "
            + ", ".join(missing_sections)
            + "."
        )

    if score < 70:
        improvements.append(
            "Review the resume score breakdown and improve the "
            "areas with lower scores."
        )

    if not contact_data.get("email"):
        improvements.append(
            "Add a clearly formatted email address."
        )

    if not contact_data.get("phone"):
        improvements.append(
            "Add a valid 10-digit phone number."
        )

    if not details.get("action_verbs"):
        improvements.append(
            "Use specific action verbs to describe your work "
            "and project contributions."
        )

    if len(skills) < 5:
        improvements.append(
            "Include relevant technical skills that you can "
            "demonstrate through your experience or projects."
        )

    if not improvements:
        improvements.append(
            "Continue tailoring your resume to the requirements "
            "of each role you apply for."
        )

    return improvements


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Resume Analyzer API is running",
        "status": "success"
    }), 200


# --------------------------------------------------
# Resume analysis route
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    filepath = None

    try:
        # Check whether a file was uploaded.
        if "resume" not in request.files:
            return jsonify({
                "error": "No resume file was uploaded."
            }), 400

        file = request.files["resume"]

        if not file or not file.filename:
            return jsonify({
                "error": "Please select a PDF resume."
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "error": "Only PDF files are supported."
            }), 400

        # Create a safe, unique filename.
        original_filename = secure_filename(file.filename)

        if not original_filename:
            return jsonify({
                "error": "The uploaded filename is invalid."
            }), 400

        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        file.save(filepath)

        # Extract text from the PDF.
        resume_text = extract_pdf_text(filepath)

        if not resume_text:
            return jsonify({
                "error": (
                    "No readable text was found in this PDF. "
                    "Try uploading a text-based PDF resume."
                )
            }), 400

        # Calculate the score using predefined rules.
        score, score_details = calculate_ats_score(resume_text)

        # Extract skills and recommend career paths.
        skills = extract_skills(resume_text)

        career_recommendations = recommend_jobs(skills)

        # Prepare a roadmap for the highest-matching role.
        roadmap = []

        if career_recommendations:
            best_career = career_recommendations[0]["role"]
            roadmap = create_roadmap(best_career)

        # Generate strengths and improvement suggestions.
        strengths = build_strengths(
            score,
            score_details,
            skills
        )

        improvements = build_improvements(
            score,
            score_details,
            skills
        )

        created_at = datetime.now(timezone.utc).isoformat()

        # Store the complete result as ONE dictionary.
        # This matches save_analysis(result) in database.py.
        analysis_result = {
            "filename": original_filename,
            "created_at": created_at,
            "score": score,
            "word_count": score_details.get("word_count", 0),
            "skills_found": skills,
            "strengths": strengths,
            "improvements": improvements,
            "career_recommendations": career_recommendations,
            "roadmap": roadmap,
            "analysis_details": score_details
        }

        # Save the analysis and obtain its database ID.
        history_id = save_analysis(analysis_result)

        # Return the analysis to the frontend.
        response_data = {
            "id": history_id,
            **analysis_result
        }

        return jsonify(response_data), 200

    except Exception as error:
        app.logger.exception("Resume analysis failed")

        return jsonify({
            "error": "The resume could not be analyzed.",
            "details": str(error)
        }), 500

    finally:
        # Remove the temporary PDF after processing.
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                app.logger.warning(
                    "Could not remove temporary upload: %s",
                    filepath
                )


# --------------------------------------------------
# Analysis history route
# --------------------------------------------------

@app.route("/history", methods=["GET"])
def analysis_history():
    try:
        history = get_history()
        return jsonify(history), 200

    except Exception as error:
        app.logger.exception("Could not load analysis history")

        return jsonify({
            "error": "Could not load analysis history.",
            "details": str(error)
        }), 500


# --------------------------------------------------
# Get one saved analysis
# --------------------------------------------------

@app.route("/history/<int:analysis_id>", methods=["GET"])
def get_saved_analysis(analysis_id):
    try:
        analysis = get_analysis(analysis_id)

        if analysis is None:
            return jsonify({
                "error": "Analysis not found."
            }), 404

        return jsonify(analysis), 200

    except Exception as error:
        app.logger.exception("Could not load saved analysis")

        return jsonify({
            "error": "Could not load this analysis.",
            "details": str(error)
        }), 500


# --------------------------------------------------
# Delete an analysis from history
# --------------------------------------------------

@app.route("/history/<int:analysis_id>", methods=["DELETE"])
def remove_saved_analysis(analysis_id):
    try:
        deleted = delete_analysis(analysis_id)

        if not deleted:
            return jsonify({
                "error": "Analysis not found."
            }), 404

        return jsonify({
            "message": "Analysis deleted successfully.",
            "id": analysis_id
        }), 200

    except Exception as error:
        app.logger.exception("Could not delete analysis")

        return jsonify({
            "error": "Could not delete this analysis.",
            "details": str(error)
        }), 500


# --------------------------------------------------
# Get a roadmap for a selected career
# --------------------------------------------------

@app.route("/roadmap/<path:career>", methods=["GET"])
def get_career_roadmap(career):
    try:
        roadmap = create_roadmap(career)

        if not roadmap:
            return jsonify({
                "error": "No roadmap is available for this career."
            }), 404

        return jsonify({
            "career": career,
            "roadmap": roadmap
        }), 200

    except Exception as error:
        app.logger.exception("Could not generate career roadmap")

        return jsonify({
            "error": "Could not load the career roadmap.",
            "details": str(error)
        }), 500


# --------------------------------------------------
# File size error handler
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "The PDF is too large. Maximum allowed size is 10 MB."
    }), 413


# --------------------------------------------------
# Start the server
# ----------------------------------a----------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )