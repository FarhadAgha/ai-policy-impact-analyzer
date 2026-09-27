"""
dashboard_sections.py

Defines the fixed set of questions that get run automatically
against the uploaded document to populate the dashboard, mirroring
the structure from the project spec (Policy Overview, Requirements,
Stakeholder Impact, etc.).
"""

DASHBOARD_SECTIONS = {
    "Policy Overview": (
        "What is the title, issuing organization, date, jurisdiction, "
        "policy type, main objective, scope, and target entities of this "
        "document? If any of these are not stated, say so explicitly "
        "rather than guessing."
    ),
    "Key Requirements": (
        "What are the main requirements or obligations this policy "
        "imposes? For each one, state who it applies to and what action "
        "is required."
    ),
    "Stakeholder Impact": (
        "How might this policy affect different stakeholders — "
        "government/regulators, AI companies, businesses/employers, "
        "developers, researchers, consumers/citizens, civil society, and "
        "small/medium enterprises? Use hedged language ('may affect', "
        "'could create') rather than certain predictions."
    ),
    "Policy Dimensions": (
        "How does this policy address safety, transparency, "
        "accountability, privacy/data protection, fairness/bias, human "
        "oversight, and security? For any dimension not addressed, say "
        "so explicitly."
    ),
    "Potential Benefits": (
        "What potential benefits does this policy state or reasonably "
        "support? Separate benefits the document explicitly states from "
        "benefits that are your own analytical inference."
    ),
    "Potential Concerns": (
        "What potential concerns, trade-offs, or implementation "
        "questions does this policy raise — such as compliance burden, "
        "cost, regulatory uncertainty, or ambiguous requirements? Present "
        "these neutrally, not as failures."
    ),
        "Policy Trade-offs": (
        "What tensions or trade-offs does this policy involve — such as "
        "innovation vs. regulation, safety vs. speed of deployment, "
        "transparency vs. confidentiality, compliance vs. cost, or "
        "central oversight vs. organizational flexibility? Explain each "
        "trade-off neutrally without declaring a winner."
    ),
    "Implementation Challenges": (
        "What does this policy specify about enforcement responsibility, "
        "required resources, technical standards, reporting mechanisms, "
        "penalties, timelines, and monitoring? Distinguish what is "
        "explicitly specified from open implementation questions."
    ),
}