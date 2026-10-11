ROADMAPS = {

    "Frontend Developer": [

        {
            "title": "Strengthen Current Skills",

            "items": [
                "HTML",
                "CSS",
                "JavaScript"
            ]
        },

        {
            "title": "Learn Advanced Skills",

            "items": [
                "React",
                "TypeScript",
                "Testing"
            ]
        },

        {
            "title": "Build Projects",

            "items": [
                "E-commerce website",
                "Dashboard",
                "Portfolio"
            ]
        },

        {
            "title": "Career Preparation",

            "items": [
                "GitHub portfolio",
                "Resume improvement",
                "Interview preparation"
            ]
        }

    ],


    "Python Developer": [

        {
            "title": "Strengthen Python",

            "items": [
                "Python fundamentals",
                "OOP",
                "Error handling"
            ]
        },

        {
            "title": "Backend Development",

            "items": [
                "Flask",
                "APIs",
                "SQL"
            ]
        },

        {
            "title": "Build Projects",

            "items": [
                "REST API",
                "Authentication system",
                "Backend application"
            ]
        },

        {
            "title": "Career Preparation",

            "items": [
                "GitHub",
                "Resume",
                "Interview preparation"
            ]
        }

    ],


    "Data Analyst": [

        {
            "title": "Data Fundamentals",

            "items": [
                "Python",
                "Statistics",
                "SQL"
            ]
        },

        {
            "title": "Data Analysis",

            "items": [
                "Pandas",
                "NumPy",
                "Data visualization"
            ]
        },

        {
            "title": "Build Projects",

            "items": [
                "Sales dashboard",
                "Customer analysis",
                "Data cleaning project"
            ]
        },

        {
            "title": "Career Preparation",

            "items": [
                "Portfolio",
                "Resume",
                "Interview preparation"
            ]
        }

    ],


    "Full Stack Developer": [

        {
            "title": "Strengthen Frontend Skills",

            "items": [
                "HTML",
                "CSS",
                "JavaScript",
                "React"
            ]
        },

        {
            "title": "Learn Backend Development",

            "items": [
                "Node.js",
                "Express",
                "REST APIs",
                "MongoDB"
            ]
        },

        {
            "title": "Build Full Stack Projects",

            "items": [
                "E-commerce application",
                "Authentication system",
                "Full stack dashboard"
            ]
        },

        {
            "title": "Career Preparation",

            "items": [
                "GitHub portfolio",
                "Resume improvement",
                "Interview preparation"
            ]
        }

    ]

}


def create_roadmap(career):

    return ROADMAPS.get(
        career,
        []
    )