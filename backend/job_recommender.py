CAREER_ROLES = {

    "Frontend Developer": [

        "html",
        "css",
        "javascript",
        "react",
        "typescript",
        "tailwind"

    ],


    "Python Developer": [

        "python",
        "flask",
        "django",
        "sql",
        "git"

    ],


    "Data Analyst": [

        "python",
        "pandas",
        "numpy",
        "sql",
        "data analysis",
        "matplotlib"

    ],


    "Full Stack Developer": [

        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "express",
        "mongodb"

    ]

}


def recommend_jobs(found_skills):

    found_skills = [
        skill.lower()
        for skill in found_skills
    ]


    recommendations = []


    for role, required_skills in CAREER_ROLES.items():

        matched = []


        for skill in required_skills:

            if skill.lower() in found_skills:

                matched.append(skill)


        total = len(required_skills)


        percentage = int(
            (len(matched) / total) * 100
        )


        missing = [

            skill

            for skill in required_skills

            if skill not in matched

        ]


        recommendations.append({

            "role": role,

            "match": percentage,

            "matched_skills": matched,

            "missing_skills": missing

        })


    recommendations.sort(
        key=lambda x: x["match"],
        reverse=True
    )


    return recommendations