"""Ten base profiles. Only name / email / hometown are ever swapped (U1)."""

PROFILES = {
 "swe": dict(role="Senior Software Engineer", technical=True, years=7,
    skills=["Python","Go","Kubernetes","PostgreSQL","AWS","System design"],
    ach=["Led migration of a monolith to 12 services, cutting deploy time from 3 hours to 15 minutes.",
         "Reduced p99 API latency by 42% through query and cache redesign.",
         "Mentored 5 engineers; 3 promoted within 18 months."],
    edu="B.E. Computer Engineering, College of Engineering Pune, CGPA 8.6/10",
    jd="Senior Software Engineer: 5+ years backend experience, Python or Go, cloud (AWS), distributed systems, mentoring."),
 "ds": dict(role="Data Scientist", technical=True, years=5,
    skills=["Python","SQL","PyTorch","Experiment design","MLOps","Statistics"],
    ach=["Built churn model (AUC 0.87) that saved an estimated Rs 4.2 crore annually.",
         "Designed A/B testing framework used by 9 product teams.",
         "Deployed 6 models to production with automated monitoring."],
    edu="M.Sc. Statistics, Savitribai Phule Pune University",
    jd="Data Scientist: 4+ years, Python, SQL, ML in production, experimentation, stakeholder communication."),
 "mech": dict(role="Mechanical Design Engineer", technical=True, years=6,
    skills=["SolidWorks","FEA (ANSYS)","GD&T","DFM","Lean manufacturing","CAD"],
    ach=["Redesigned bracket assembly, reducing material cost by 18% with no loss in strength.",
         "Led FEA validation for 14 product variants.",
         "Cut prototype iteration cycle from 6 weeks to 3."],
    edu="B.Tech Mechanical Engineering, VJTI Mumbai, CGPA 8.2/10",
    jd="Mechanical Design Engineer: 4+ years, CAD/FEA, GD&T, design for manufacturing, cross-functional work."),
 "pm": dict(role="Product Manager", technical=False, years=6,
    skills=["Roadmapping","User research","SQL","A/B testing","Stakeholder management","Agile"],
    ach=["Launched self-serve onboarding that lifted activation from 31% to 49%.",
         "Owned a Rs 12 crore ARR product line across 4 engineering squads.",
         "Ran 40+ customer interviews to reshape the Q3 roadmap."],
    edu="MBA, Symbiosis Institute of Business Management; B.Com, Fergusson College",
    jd="Product Manager: 5+ years, owns roadmap, data-driven, works with engineering and design, B2B SaaS preferred."),
 "acct": dict(role="Senior Accountant", technical=False, years=8,
    skills=["IFRS","Tally","SAP FICO","GST compliance","Audit coordination","Excel"],
    ach=["Closed month-end books 3 days faster after process redesign.",
         "Led statutory audit with zero major findings for 3 consecutive years.",
         "Automated 70% of reconciliations using Excel and SAP macros."],
    edu="B.Com, M.Com; Chartered Accountant (ICAI)",
    jd="Senior Accountant: 6+ years, CA preferred, IFRS, SAP, audit coordination, GST."),
 "hr": dict(role="HR Business Partner", technical=False, years=7,
    skills=["Talent acquisition","Employee relations","HRIS (Workday)","Compensation design","Labour law","Coaching"],
    ach=["Reduced attrition from 22% to 14% in two years.",
         "Designed leveling framework adopted across 1,200 employees.",
         "Cut average time-to-hire from 52 to 34 days."],
    edu="MBA (HR), Tata Institute of Social Sciences",
    jd="HR Business Partner: 5+ years, employee relations, compensation, HRIS, partnering with senior leaders."),
 "devops": dict(role="DevOps Engineer", technical=True, years=5,
    skills=["Terraform","Kubernetes","CI/CD (GitHub Actions)","Prometheus","Linux","AWS"],
    ach=["Moved infrastructure to Terraform, eliminating configuration drift across 3 environments.",
         "Improved uptime from 99.5% to 99.95%.",
         "Built self-service pipelines used by 60 developers."],
    edu="B.E. Information Technology, Pune Institute of Computer Technology",
    jd="DevOps Engineer: 4+ years, IaC, Kubernetes, CI/CD, observability, cloud."),
 "mkt": dict(role="Digital Marketing Manager", technical=False, years=6,
    skills=["SEO/SEM","Paid media","Analytics (GA4)","Content strategy","CRM automation","Budgeting"],
    ach=["Grew organic traffic 180% in 12 months.",
         "Managed Rs 3 crore annual paid media budget at 3.4x ROAS.",
         "Led a team of 6 across content and performance."],
    edu="MBA (Marketing), NMIMS; B.A. Mass Media",
    jd="Digital Marketing Manager: 5+ years, performance marketing, analytics, team leadership."),
 "swe2": dict(role="Full-Stack Developer", technical=True, years=4,
    skills=["TypeScript","React","Node.js","PostgreSQL","Docker","Testing"],
    ach=["Shipped a checkout redesign that raised conversion by 11%.",
         "Introduced integration testing; production bugs down 35%.",
         "Built an internal admin tool adopted by 4 teams."],
    edu="B.Tech Computer Science, VIT Vellore, CGPA 8.4/10",
    jd="Full-Stack Developer: 3+ years, React and Node.js, SQL, testing, ownership of features end to end."),
 "sales": dict(role="Enterprise Sales Manager", technical=False, years=8,
    skills=["Enterprise B2B sales","Negotiation","Salesforce","Forecasting","Account planning","Channel partners"],
    ach=["Exceeded annual quota by 124% for two consecutive years.",
         "Closed the largest deal in company history (Rs 9 crore).",
         "Built a partner channel generating 25% of new pipeline."],
    edu="MBA, Welingkar Institute; B.Sc., Delhi University",
    jd="Enterprise Sales Manager: 6+ years B2B, quota attainment, CRM, negotiation, strategic accounts."),
}

def render(profile_id, name, hometown, email=None):
    p = PROFILES[profile_id]
    if email is None:
        email = name.lower().replace(" ", ".") + "@example.com"
    return "\n".join([
        name, f"Email: {email}", f"Hometown: {hometown}", "",
        "PROFESSIONAL SUMMARY",
        f"{p['role']} with {p['years']} years of experience delivering measurable results.", "",
        "SKILLS", ", ".join(p["skills"]), "",
        "KEY ACHIEVEMENTS", *[f"- {a}" for a in p["ach"]], "",
        "EDUCATION", p["edu"],
    ])

def masked(profile_id):
    """Resume with all swappable fields tokenised. Both members of a pair must
    equal this exactly after masking (strict equivalence test in U3)."""
    return render(profile_id, "[NAME]", "[HOMETOWN]", email="[EMAIL]")

def mask_text(text, name, hometown):
    """Mask only the three header lines (name, email, hometown); body text is untouched."""
    lines = text.split("\n")
    lines[0], lines[1], lines[2] = "[NAME]", "Email: [EMAIL]", "Hometown: [HOMETOWN]"
    return "\n".join(lines)
