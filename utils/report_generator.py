from fpdf import FPDF


def generate_report(
        role,
        ats_score,
        matched_skills,
        missing_skills):

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.cell(190, 10, "ResumeIQ Professional ATS Report", ln=True)

    pdf.ln(5)

    # Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Resume Summary", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 8, f"Target Role: {role}", ln=True)
    pdf.cell(190, 8, f"ATS Score: {ats_score}%", ln=True)

    pdf.ln(5)

    # Strengths
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Matched Skills", ln=True)

    pdf.set_font("Arial", "", 12)

    for skill in matched_skills:
        pdf.cell(190, 8, f"+ {skill}", ln=True)

    pdf.ln(3)

    # Weaknesses
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Missing Skills", ln=True)

    pdf.set_font("Arial", "", 12)

    for skill in missing_skills:
        pdf.cell(190, 8, f"- {skill}", ln=True)

    pdf.ln(5)

    # Suggestions
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Recommendations", ln=True)

    pdf.set_font("Arial", "", 12)

    pdf.multi_cell(
        190,
        8,
        "Add missing skills, improve project descriptions, "
        "include GitHub links, certifications, and measurable achievements."
    )

    pdf.ln(5)

    # Final Verdict
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Final Verdict", ln=True)

    pdf.set_font("Arial", "", 12)

    if ats_score >= 80:
        verdict = "Excellent Resume"
    elif ats_score >= 60:
        verdict = "Good Resume"
    elif ats_score >= 40:
        verdict = "Average Resume"
    else:
        verdict = "Needs Improvement"

    pdf.cell(190, 8, verdict, ln=True)

    file_name = "resume_report.pdf"

    pdf.output(file_name)

    return file_name