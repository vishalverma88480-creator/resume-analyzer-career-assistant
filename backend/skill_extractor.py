SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "react",
    "next.js",

    "html",
    "css",
    "tailwind",

    "node.js",
    "express",

    "mongodb",
    "mysql",
    "sql",
    "postgresql",

    "flask",
    "django",

    "git",
    "github",
    "docker",
    "aws",

    "pandas",
    "numpy",
    "matplotlib",

    "data analysis",

    "figma",
    "canva"
]


def extract_skills(text):

    text_lower = text.lower()

    found_skills = []


    for skill in SKILLS:

        if skill.lower() in text_lower:

            found_skills.append(skill)


    return found_skills