"""
MBA Company Analyzer, an MCP server for the Claude / Anthropic framework.

A pocket business school. It gives Claude the Harvard and IPADE case canon as
structured frameworks, scoring rubrics, and comparison scaffolds, so a student
can analyze and compare three or more companies (real or invented) and then face
the deepest question of the age of AI: when a machine can do most of the work,
would you still be inspired enough to build it for the next ten years?

Grounded in the value triangle, value based pricing, the Techstars pitch, and
the principle of IPADE founder Carlos Llano Cifuentes: "La empresa es la sombra
alargada del CEO." The company is the elongated shadow of the CEO.

Run: python3 server.py   (stdio transport)
"""
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from mcp.server.fastmcp import FastMCP  # noqa: E402

mcp = FastMCP("mba")

DISCLAIMER = (
    "Educational framework for class discussion, not investment, legal, or "
    "financial advice. The analyzer supplies the questions and the scoring "
    "structure; the judgment about a real company is yours to make and defend."
)


def _j(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# THE CANON
# ---------------------------------------------------------------------------

CARLOS_LLANO = {
    "quote_es": "La empresa es la sombra alargada del CEO.",
    "author": "Carlos Llano Cifuentes, founder of IPADE Business School",
    "translation_en": "The company is the elongated shadow of the CEO.",
    "meaning": (
        "A company inevitably takes the shape, the values, the strengths, and "
        "the blind spots of the person who leads it. Its culture, its ethics, "
        "and its destiny are a projection of the founder's character and "
        "motivation. So 'why you' is not a soft question. It is the most "
        "predictive one. Before you ask whether a business is viable, ask "
        "whether it is a shadow you would be proud to cast."
    ),
}

FRAMEWORKS = {
    "value_triangle": {
        "title": "The Value Triangle: three kinds of value a customer receives",
        "definition": (
            "A customer never buys a product. They buy value, and value has "
            "three faces. The strongest companies deliver all three. The most "
            "beloved brands win on the third."
        ),
        "parts": {
            "Utility value (functional)": (
                "Does it do the job well? Performance, reliability, "
                "convenience, time saved. You do not buy a drill, you buy the "
                "hole."
            ),
            "Monetary value (economic)": (
                "Does it make or save money? The return on the price paid, the "
                "cost versus alternatives, the gap between willingness to pay "
                "and price."
            ),
            "Psychological value (emotional)": (
                "Does it give identity, status, belonging, meaning, delight, "
                "or trust? This is the hardest to copy and the most "
                "defensible."
            ),
        },
        "scores": "value_creation",
    },
    "value_capture": {
        "title": "Value Capture: turning value into money (pricing)",
        "definition": (
            "Creating value is not the same as capturing it. Value created is "
            "the gap between the customer's willingness to pay (WTP) and your "
            "cost. The customer keeps WTP minus price. You capture price minus "
            "cost. Pricing decides how the pie is split."
        ),
        "parts": {
            "Three ways to set price (IPADE)": (
                "(1) cost plus a margin, (2) value based, price to the value "
                "you deliver, (3) competition based, price against rivals. "
                "Value based wins when you can defend it."
            ),
            "Recurring capture": (
                "Subscription, licensing, royalties, and marketplaces capture "
                "value again and again, which beats a one time sale."
            ),
        },
        "scores": "value_capture",
    },
    "values": {
        "title": "Values: what the company actually stands for",
        "definition": (
            "A company's values are not a poster on the wall. They are the "
            "choices it makes when money and mission conflict. This is where "
            "Carlos Llano's principle bites: the company is the elongated shadow of "
            "the CEO, so its true values are the founder's true values, made "
            "visible at scale."
        ),
        "parts": {
            "Judge by choices, not slogans": (
                "What does this company stand for, judged by what it does when "
                "it costs something? Does it give more than it takes from "
                "customers, workers, and the world? Would you be proud to run "
                "it?"
            ),
        },
        "scores": "values_ethics",
    },
    "sustainability": {
        "title": "Sustainability: will it last, and does it renew what it uses?",
        "definition": (
            "Sustainability has two meanings, and a serious founder checks "
            "both. First, business durability: can the company survive and "
            "compound for a decade? Second, social and environmental "
            "sustainability: does it deplete its resources and community, or "
            "renew them?"
        ),
        "parts": {
            "Durability": "Will this company still be here in ten years, and why?",
            "Renewal, not extraction": (
                "What resource does it consume (a planet, a community, a "
                "person's trust, its own reputation), and does it renew or "
                "deplete it? Name one measurable impact metric, with a "
                "baseline and a target."
            ),
        },
        "scores": "sustainability",
    },
    "motivation": {
        "title": "Founder Fit and Motivation: would you build it for the next ten years?",
        "definition": (
            "Many companies are viable. Few are viable FOR YOU. In the age of "
            "AI, viability is cheap and abundant, and motivation is scarce. "
            "This is the question that actually predicts whether a venture "
            "happens."
        ),
        "parts": {
            "Why you": (
                "What unfair advantage, obsession, proximity, or love do you "
                "bring that most people do not?"
            ),
            "Why now": (
                "What wave in the context, a technology, a law, a shift, just "
                "made this the moment?"
            ),
            "Philosophical alignment": (
                "Does this fit your values and the person you want to become? "
                "Would this be a shadow you are proud to cast?"
            ),
            "Energy (the ten year test)": (
                "Would you stay inspired to build this for the next ten years, through the hard "
                "middle, even when it is boring and nobody is watching?"
            ),
        },
        "scores": "founder_motivation",
    },
    "future_of_work": {
        "title": "The Future of Work: what stays human when AI can do the rest",
        "definition": (
            "As AI makes execution abundant and nearly free (writing, coding, "
            "analysis, design, routine operations), the scarce and defensible "
            "inputs invert. When the how is commoditized, the why and the who "
            "win. The moat moves from skill to motivation, taste, judgment, "
            "trust, relationships, and the will to keep going."
        ),
        "parts": {
            "Split the work into two piles": (
                "(a) AI-automatable: the execution a capable model can do. "
                "(b) Irreplaceably human: motivation, vision, taste, trust, "
                "care, accountability, and the courage to decide under "
                "uncertainty. The larger and more defensible the human pile, "
                "the more durable the venture."
            ),
        },
        "scores": "ai_resilience",
    },
    "pitch": {
        "title": "The pitch (Techstars minimal elements)",
        "definition": (
            "Once you understand the company, you have to pitch it. The "
            "Techstars format is the minimal set of things a pitch must say, "
            "in order, with one rule: every slide answers 'so what?'. If a "
            "slide does not move the story forward, cut it. Use deck_outline "
            "then pitch_deck to generate the deck."
        ),
        "parts": {
            "1. Cover": (
                "Company name and a one line pitch a stranger could repeat "
                "correctly."
            ),
            "2. Problem": (
                "The pain, who has it, how big it is, and why now. Concrete, "
                "not abstract."
            ),
            "3. Solution": (
                "What you do, how it works in about three steps, and the one "
                "aha that makes people lean in."
            ),
            "4. Market and model": (
                "TAM, SAM, SOM as three honest numbers, and how the company "
                "actually makes money."
            ),
            "5. Traction and moat": (
                "Real proof (users, revenue, pilots, milestones) and the moat "
                "a rival cannot copy."
            ),
            "6. Team and the ask": (
                "Who the team is and why them, the exact ask, and the vision "
                "if it works."
            ),
        },
        "scores": "render it with deck_outline then pitch_deck",
    },
    "case_method": {
        "title": "The IPADE case method: how to run the whole analysis",
        "definition": "Do not rush to a verdict. Diagnose, then decide, then defend.",
        "parts": {
            "1. Situation": (
                "Read the customer, the market, and the competition to find the "
                "real problem."
            ),
            "2. Alternatives": (
                "Use the value triangle and value capture to design and price "
                "courses of action."
            ),
            "3. Financials": (
                "Check the 3 R's: Recursos (resources you need), Riesgo "
                "(risk), and Rentabilidad (profitability). Then commit to the "
                "best answer and defend it. There is rarely one perfect answer."
            ),
        },
        "scores": "all",
    },
}

# Aliases so students can ask naturally.
_ALIASES = {
    "value triangle": "value_triangle", "triangle": "value_triangle",
    "value": "value_triangle", "value creation": "value_triangle",
    "value capture": "value_capture", "pricing": "value_capture",
    "price": "value_capture", "capture": "value_capture",
    "value stick": "value_capture",
    "values ": "values", "ethics": "values", "mission": "values",
    "sustainability ": "sustainability", "esg": "sustainability",
    "durability": "sustainability",
    "motivation ": "motivation", "founder": "motivation",
    "founder fit": "motivation", "why you": "motivation",
    "future of work": "future_of_work", "ai": "future_of_work",
    "automation": "future_of_work", "future": "future_of_work",
    "case method": "case_method", "method": "case_method",
    "case": "case_method",
    "pitch": "pitch", "pitch deck": "pitch", "deck": "pitch",
    "techstars": "pitch", "slides": "pitch", "presentation": "pitch",
}

DIMENSIONS = [
    {"key": "customer_market", "label": "Customer and Market"},
    {"key": "value_creation", "label": "Value Creation (value triangle)"},
    {"key": "value_capture", "label": "Value Capture (pricing)"},
    {"key": "competition_moat", "label": "Competition and Moat"},
    {"key": "values_ethics", "label": "Values and Ethics"},
    {"key": "sustainability", "label": "Sustainability and Durability"},
    {"key": "founder_motivation", "label": "Founder Fit and Motivation"},
    {"key": "ai_resilience", "label": "AI-Resilience (future of work)"},
]
def _verdict(grade: float) -> str:
    if grade >= 3.0:
        return "Compelling. This is worth building, and worth building by you."
    if grade >= 2.4:
        return ("Promising. The idea is real. Sharpen the weakest lenses and the "
                "moat before you commit.")
    if grade >= 1.8:
        return ("Viable but thin. The business could exist, but the edge or "
                "the motivation is weak. Rework it, or pick a different shadow "
                "to cast.")
    return ("Not yet. Fix the fundamentals, or choose a company you would "
            "actually be inspired to build for the next ten years.")


def _score_one(scores: dict):
    """Return (grade_1_to_4, per_dimension_list, missing_keys). Each lens is
    scored 1 to 4; the grade is the plain average of the lenses provided."""
    per = []
    got = 0.0
    n = 0
    missing = []
    for d in DIMENSIONS:
        k = d["key"]
        if k in scores and scores[k] is not None:
            try:
                v = float(scores[k])
            except (TypeError, ValueError):
                v = 1.0
            v = max(1.0, min(4.0, v))
            got += v
            n += 1
            per.append({"dimension": d["label"], "key": k, "score": round(v, 1)})
        else:
            missing.append(k)
            per.append({"dimension": d["label"], "key": k, "score": None})
    grade = round(got / n, 1) if n else 0.0
    return grade, per, missing


EXERCISE = """MBA COMPANY ANALYZER, THE STUDENT EXERCISE

Objective. Practice thinking like a founder and an investor, then discover the
one input AI cannot supply for you.

Step 1. Pick three companies. At least one real and one you invent. A strong
set is one giant, one startup, and your own idea.

Step 2. Analyze each with the tool. For each company run analyze_company, answer
the questions it returns for the value triangle, value capture, the customer and market,
values, and sustainability, then record a score from 1 to 4 on each of the
eight dimensions with score_company.

Step 3. Compare. Run compare_companies with all three scorecards. Read the
matrix. Which company wins on customer and market, on value capture, on moat?
Which is only cheap, or only clever?

Step 4. The future of work. Run future_of_work on each. Split the work into what
an AI could do tomorrow and what still needs a motivated human. Notice that the
most durable companies keep a large, human core.

Step 5. The real question. Run motivation_check on the company you would build.
Answer honestly: why you, why now, does it align with who you want to become,
and would you stay inspired to build it for the next ten years. The numbers rank viability.
This ranks you.

Step 6. Decide and defend. In one paragraph, name the company you would build
and defend the choice with the frameworks. Remember Carlos Llano: the company is
the elongated shadow of the CEO. Choose a shadow you are proud to cast.
"""


# ---------------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------------

@mcp.tool()
def status() -> str:
    """What this analyzer is and how to drive it. A pocket business school
    grounded in the Harvard and IPADE case method, for comparing three or more
    companies and deciding which one is worth building, and worth building by
    you. Start here."""
    return _j({
        "name": "MBA Company Analyzer",
        "grounding": ("Harvard and IPADE case method. The value triangle, "
                      "value based pricing, the Techstars pitch, and Carlos "
                      "Llano's principle of the elongated shadow of the CEO."),
        "epigraph": CARLOS_LLANO,
        "how_to_use": [
            "1. get_framework to learn any lens (or list_frameworks for the index).",
            "2. analyze_company(name, description) for each company to get the scaffold.",
            "3. score_company(name, scores_json) to record 1 to 4 on the eight dimensions.",
            "4. compare_companies(companies_json) to rank them on one matrix.",
            "5. future_of_work(name) to see what stays human when AI does the rest.",
            "6. motivation_check(name) for the ten year test on the one you would build.",
            "7. deck_outline() then pitch_deck(name, deck_json) to deliver the Techstars pitch deck.",
            "8. get_exercise for the full classroom exercise.",
        ],
        "dimensions": [{"key": d["key"], "label": d["label"]}
                       for d in DIMENSIONS],
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def list_frameworks() -> str:
    """List the analytical frameworks available, each with a one line summary.
    Use get_framework(name) to open any of them."""
    return _j({
        "frameworks": [{"key": k, "title": v["title"]} for k, v in FRAMEWORKS.items()],
        "tip": "get_framework('value_triangle' | 'value_capture' | 'values' | "
               "'sustainability' | 'motivation' | 'future_of_work' | 'pitch' | "
               "'case_method'), or empty for all.",
    })


@mcp.tool()
def get_framework(name: str = "") -> str:
    """Open one analytical framework in full: its definition, its parts, the
    questions to ask, and which scoring dimension it feeds. Pass a key such as
    'value_triangle', 'value_capture', 'values', 'sustainability',
    'motivation', 'future_of_work', 'pitch', or 'case_method'. Aliases like
    'pricing', 'why you', 'ai', or 'deck' also work. Pass an empty string for all."""
    q = (name or "").strip().lower()
    if not q:
        return _j({"frameworks": FRAMEWORKS, "epigraph": CARLOS_LLANO,
                   "disclaimer": DISCLAIMER})
    key = q if q in FRAMEWORKS else _ALIASES.get(q)
    if not key:
        # loose contains match
        for a, target in _ALIASES.items():
            if a.strip() and a.strip() in q:
                key = target
                break
    if not key or key not in FRAMEWORKS:
        return _j({"error": f"Unknown framework '{name}'.",
                   "available": list(FRAMEWORKS.keys())})
    return _j({"framework": FRAMEWORKS[key], "disclaimer": DISCLAIMER})


@mcp.tool()
def analyze_company(name: str, description: str = "") -> str:
    """Build a rigorous analysis scaffold for one company (real or invented).
    Returns the lens by lens questions to answer for this specific company
    across every framework, plus a blank 1 to 4 scoring template. This tool
    supplies the structure and the questions. You supply the reasoning about the
    real company, then record the result with score_company."""
    lenses = []
    for key, fw in FRAMEWORKS.items():
        if key == "case_method":
            continue
        lenses.append({
            "framework": fw["title"],
            "consider": fw["definition"],
            "answer_for_this_company": list(fw.get("parts", {}).keys()),
        })
    return _j({
        "company": name,
        "description": description or "(none provided; reason from what you know)",
        "instructions": (
            "Answer each lens below specifically for this company. Be concrete, "
            "cite the single strongest piece of evidence behind each claim, and "
            "answer 'so what?' for every point, cut anything that does not change "
            "the decision. Do not invent precise financials you do not have; "
            "reason from the business model and hedge honestly."
        ),
        "lenses": lenses,
        "sharpen_the_analysis": {
            "so_what": "For every lens, state why it changes the decision.",
            "bull_case": "The strongest one paragraph reason this becomes a big company.",
            "bear_case": "The strongest one paragraph reason it fails.",
            "key_metric": "The one number that, if it moves, decides everything.",
            "confidence": "Rate your confidence 1 to 4 and say what evidence would raise it.",
        },
        "scoring_template": {d["key"]: None for d in DIMENSIONS},
        "scoring_guide": {d["key"]: d["label"] for d in DIMENSIONS},
        "deliver": [
            "1. score_company(name, scores_json) for the 1 to 4 scorecard.",
            "2. compare_companies(companies_json) to rank the set.",
            "3. deck_outline() then pitch_deck(name, deck_json) to deliver the Techstars HTML pitch deck.",
        ],
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def score_company(name: str, scores_json: str) -> str:
    """Record a company's scorecard and get a grade from 1 to 4 and a verdict.
    Pass scores_json as a JSON object mapping dimension keys to numbers from 1
    to 4 (1 weak, 2 fair, 3 strong, 4 exceptional), for example:
    {"customer_market": 3, "value_creation": 3, "value_capture": 2,
    "competition_moat": 3, "values_ethics": 4, "sustainability": 3,
    "founder_motivation": 4, "ai_resilience": 3}. Missing dimensions are
    allowed and are averaged out."""
    try:
        scores = json.loads(scores_json)
        if not isinstance(scores, dict):
            raise ValueError("scores_json must be a JSON object")
    except (json.JSONDecodeError, ValueError) as e:
        return _j({"error": f"Could not parse scores_json: {e}",
                   "expected_keys": [d["key"] for d in DIMENSIONS]})
    total, per, missing = _score_one(scores)
    return _j({
        "company": name,
        "grade_1_to_4": total,
        "verdict": _verdict(total),
        "per_dimension": per,
        "missing_dimensions": missing,
        "note": ("The grade ranks viability. It does not decide motivation. Run "
                 "motivation_check before you commit."),
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def compare_companies(companies_json: str) -> str:
    """Compare two to four scored companies on one matrix. Pass companies_json
    as a JSON array of objects, each with a name and a scores object, for
    example: [{"name":"A","scores":{"customer_market":3,...}}, {"name":"B",
    "scores":{...}}]. Returns a dimension by company matrix, the leader on each
    dimension, the overall ranking, and a decision scaffold."""
    try:
        companies = json.loads(companies_json)
        if not isinstance(companies, list) or not companies:
            raise ValueError("companies_json must be a non empty JSON array")
    except (json.JSONDecodeError, ValueError) as e:
        return _j({"error": f"Could not parse companies_json: {e}",
                   "expected": '[{"name":"A","scores":{"customer_market":3,...}}, ...]'})
    computed = []
    for c in companies[:4]:
        nm = c.get("name", "Company")
        total, per, _ = _score_one(c.get("scores", {}))
        computed.append({"name": nm, "total": total,
                         "scores": {p["key"]: p["score"] for p in per}})
    names = [c["name"] for c in computed]
    matrix = []
    for d in DIMENSIONS:
        row = {"dimension": d["label"]}
        best_name, best_val = None, -1.0
        for c in computed:
            v = c["scores"].get(d["key"])
            row[c["name"]] = v
            if v is not None and v > best_val:
                best_val, best_name = v, c["name"]
        row["leader"] = best_name
        matrix.append(row)
    ranking = sorted(computed, key=lambda c: c["total"], reverse=True)
    return _j({
        "companies": names,
        "matrix": matrix,
        "ranking": [{"rank": i + 1, "name": c["name"], "grade_1_to_4": c["total"],
                     "verdict": _verdict(c["total"])}
                    for i, c in enumerate(ranking)],
        "decision_scaffold": (
            "The ranking measures viability, not destiny. Two moves finish the "
            "analysis. First, if the top two are close, break the tie with the "
            "future of work: which one keeps the larger human core when AI "
            "commoditizes execution. Second, override the numbers with the "
            "ten year test: among the viable companies, which one would you "
            "be truly motivated to build, for years, through the hard middle? "
            "Why you? Why now? Carlos Llano: the company is the elongated shadow of "
            "the CEO. Rank by the head, decide with the whole person."
        ),
        "epigraph": CARLOS_LLANO,
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def motivation_check(name: str) -> str:
    """The ten year test for the company you would actually build. Returns
    the four founder questions specialized to this company (why you, why now,
    philosophical alignment, energy), a self scoring rubric, and the Carlos Llano
    anchor. This is the input AI cannot supply for you."""
    fw = FRAMEWORKS["motivation"]
    return _j({
        "company": name,
        "premise": fw["definition"],
        "answer_honestly": {
            "why_you": fw["parts"]["Why you"],
            "why_now": fw["parts"]["Why now"],
            "philosophical_alignment": fw["parts"]["Philosophical alignment"],
            "energy": fw["parts"]["Energy (the ten year test)"],
        },
        "self_score_0_to_10": {
            "unfair_advantage": "How real is your edge for this?",
            "why_now": "How strong is the timing wave?",
            "values_alignment": "How well does it fit who you want to become?",
            "durable_energy": "Would you still want it in year three?",
        },
        "interpretation": (
            "If any of these is low, no business plan will save it. A brilliant "
            "idea you feel lukewarm about should score low, and that is the "
            "tool working. Feed the average of these into founder_motivation."
        ),
        "epigraph": CARLOS_LLANO,
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def future_of_work(name: str) -> str:
    """Assess a company through the future of work lens. Returns the method for
    splitting its work into what AI can automate and what stays irreplaceably
    human, the questions to answer, and the thesis that in the age of AI the
    moat moves from skill to motivation, taste, trust, and judgment. Feeds the
    ai_resilience dimension."""
    fw = FRAMEWORKS["future_of_work"]
    return _j({
        "company": name,
        "thesis": fw["definition"],
        "method": fw["parts"]["Split the work into two piles"],
        "answer_for_this_company": [
            "If a strong AI joined this company tomorrow, which tasks would it do well?",
            "Which tasks still require a motivated human, and exactly why?",
            "What is left that only a founder who deeply cares can do?",
            "Is that human core the company's moat, or an afterthought?",
        ],
        "scoring": (
            "Score ai_resilience high when the company's core value depends on "
            "human motivation, trust, taste, or judgment that AI amplifies but "
            "cannot replace. Score low when the whole company is execution that "
            "a model will soon do for nearly free."
        ),
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def carlos_llano_principle() -> str:
    """The founding principle behind the whole analyzer. Carlos Llano, founder
    of IPADE: 'La empresa es la sombra alargada del CEO', with its English
    translation and what it means for choosing which company to build."""
    return _j({"principle": CARLOS_LLANO, "disclaimer": DISCLAIMER})


@mcp.tool()
def get_exercise() -> str:
    """The full student exercise, six steps, from analyzing three companies to
    the ten year test. Hand this to a class, or run it yourself."""
    return _j({"exercise": EXERCISE, "epigraph": CARLOS_LLANO,
               "repo": "https://github.com/duribebe/mba-mcp", "disclaimer": DISCLAIMER})


@mcp.tool()
def rebut(position: str) -> str:
    """Adversarial sparring. Paste a claim a student makes about a company (for
    example 'this has a huge moat' or 'customers will happily pay 50 dollars a
    month'). Returns the sharpest objections a skeptical investor or board
    member would raise, so the claim can be hardened before it is believed."""
    return _j({
        "claim": position,
        "pressure_test_from": [
            "Customer (DMU): is the payer the same as the user, and is their "
            "willingness to pay proven or assumed?",
            "Competition and moat: what stops a well funded rival, or a large "
            "platform, from copying this next quarter?",
            "Value capture: even if the value is real, can you charge for it, "
            "and defend the margin, or does competition drive price to cost?",
            "Context and why now: is the timing a genuine wave, or wishful "
            "thinking? What has to be true about the world for this to work?",
            "Future of work: how much of this is execution an AI will soon do "
            "for nearly free, collapsing your advantage?",
            "Motivation: is the founder's energy real and durable, or is this "
            "a spreadsheet no one will be inspired to build for the next ten years?",
        ],
        "instruction": ("Voice the single toughest objection above in the voice "
                        "of a skeptical investor, then say what evidence would "
                        "actually answer it."),
        "disclaimer": DISCLAIMER,
    })


# ---------------------------------------------------------------------------
# TECHSTARS PITCH DECK  (delivers a self-contained .html deck, 5 to 6 slides)
# ---------------------------------------------------------------------------

TECHSTARS_DECK = {
    "source": "The Techstars pitch format (Problem, Solution/Demo, Traction, "
              "Business Model, Market, Marketing/Sales, Team, The Ask, Vision), "
              "distilled to 6 slides.",
    "golden_rule": "Every slide must answer 'so what?'. If a slide does not push "
                   "the story forward, cut it.",
    "slides": [
        {"n": 1, "title": "Cover",
         "techstars": "Who you are in one breath.",
         "put_here": "Company name, a one line pitch a stranger could repeat "
                     "correctly, and an optional tagline."},
        {"n": 2, "title": "Problem",
         "techstars": "Make them feel the pain.",
         "put_here": "The pain, who has it, how big it is, and why now. Concrete, "
                     "not abstract."},
        {"n": 3, "title": "Solution",
         "techstars": "Stop telling, start showing.",
         "put_here": "What you do, how it works in about three steps, and the one "
                     "aha that makes people lean in."},
        {"n": 4, "title": "Market and business model",
         "techstars": "Get real about size, then show the money flows.",
         "put_here": "TAM, SAM, SOM as three honest numbers, and how the company "
                     "actually makes money."},
        {"n": 5, "title": "Traction and moat",
         "techstars": "Prove you are not guessing, and say why you win.",
         "put_here": "Real proof (users, revenue, pilots, milestones) and the moat "
                     "a rival cannot copy."},
        {"n": 6, "title": "Team and the ask",
         "techstars": "Put faces to the story, be specific, end with the dream.",
         "put_here": "Who the team is and why them, exactly what you are asking "
                     "for, and the vision if it works."},
    ],
}

DECK_SCHEMA_EXAMPLE = {
    "company": "FaceVault",
    "one_liner": "A consent gate that lets anyone license their own face to apps "
                 "and AI, and revoke it in one click.",
    "tagline": "Own your likeness.",
    "accent": "#8C1515",
    "problem": {
        "headline": "Your face is used without your say, and you cannot take it back.",
        "points": ["Deepfakes and AI avatars train on faces scraped without consent.",
                   "Athletes and creators have no simple way to license or revoke a likeness."],
        "why_now": "New likeness laws in Denmark, Tennessee, and the EU just made consent enforceable."},
    "solution": {
        "headline": "A revocable license for your face, enforced in code.",
        "how": ["You mint a FaceNFT that carries your license terms.",
                "Apps and AI must present a valid, unrevoked license before they may read your face.",
                "Revoke with one signature and the gate closes."],
        "aha": "The rule is not a policy anyone can ignore, it is a lock on the only door."},
    "market": {"tam": "76.8B, biometric and likeness data by 2030",
               "sam": "8B, creators and athletes",
               "som": "50M, year one design partners",
               "note": "Built bottom up from paying design partners, not top down."},
    "business_model": {"headline": "The owner gets paid every time the face is used.",
                       "streams": ["A fee on each licensed use, split 95 percent to the person, 5 percent to the network.",
                                   "A subscription for pro creators and their agents."]},
    "traction": {"headline": "Early proof it works.",
                 "proof": ["Working prototype live.", "Three design partners signed.",
                           "First licensed use processed on chain."]},
    "moat": {"headline": "The moat is trust, not code.",
             "why_you_win": ["Enforcement lives in the read path, not in a promise.",
                             "A revocable, consented registry a bigger platform cannot fake."]},
    "team": {"headline": "Built by people who obsess over this.",
             "members": ["Founder, a builder who could not stop thinking about who owns a face.",
                         "Advisor, a likeness law attorney."]},
    "ask": {"headline": "The ask.",
            "ask": "Raising a small pre seed to reach 25 paying creators.",
            "use_of_funds": ["Engineering, the enforcement gate.", "Design partners and legal review."]},
    "vision": "A world where every person, and every AI, must ask before they use your face.",
}


def _esc(s) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _slug(name) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")
    return s or "company"


def _lis(items) -> str:
    return "".join("<li>%s</li>" % _esc(x) for x in (items or []) if str(x).strip())


_DECK_CSS = """
:root{--a:__ACCENT__;}
*{box-sizing:border-box;}
html,body{margin:0;}
body{background:#e8e8ec;font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;color:#15171d;}
.deck{min-height:100vh;display:flex;align-items:center;justify-content:center;}
.slide{display:none;position:relative;width:min(94vw,1180px);aspect-ratio:16/9;background:#fff;border-radius:14px;box-shadow:0 20px 64px rgba(0,0,0,.22);padding:5.2% 6.2%;overflow:hidden;}
.slide.active{display:flex;flex-direction:column;justify-content:center;}
.lab{position:absolute;top:5.2%;left:6.2%;font:700 12px/1 'Space Mono',ui-monospace,monospace;letter-spacing:.13em;text-transform:uppercase;color:var(--a);}
.body{margin:auto 0;width:100%;}
.kicker{font:700 13px/1 ui-monospace,monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--a);margin-bottom:16px;}
.co{font-size:clamp(34px,6.2vw,76px);font-weight:800;letter-spacing:-.02em;line-height:1.02;margin:0 0 16px;}
.one{font-size:clamp(18px,2.6vw,31px);line-height:1.28;max-width:24ch;margin:0;color:#2a2d34;}
.tag{margin-top:16px;font-size:16px;color:var(--a);font-weight:700;letter-spacing:.02em;}
h2{font-size:clamp(24px,3.7vw,44px);font-weight:800;letter-spacing:-.01em;line-height:1.08;margin:0 0 20px;max-width:20ch;}
.h3{font-size:clamp(17px,2.1vw,24px);font-weight:800;margin:0 0 12px;color:var(--a);}
ul,ol{margin:0;padding-left:1.15em;}
li{font-size:clamp(15px,1.95vw,22px);line-height:1.42;margin:0 0 10px;max-width:36ch;}
.call{margin-top:22px;border-left:5px solid var(--a);background:#f7efef;padding:13px 17px;border-radius:0 9px 9px 0;font-size:clamp(15px,1.95vw,21px);line-height:1.4;}
.call b{color:var(--a);}
.call ul{margin:9px 0 0;}
.nums{display:flex;gap:26px;flex-wrap:wrap;margin:4px 0 6px;}
.num{flex:1;min-width:150px;}
.nlab{font:700 12px/1 ui-monospace,monospace;letter-spacing:.13em;color:var(--a);margin-bottom:7px;}
.nval{font-size:clamp(17px,2.3vw,27px);font-weight:800;line-height:1.16;}
.note{font-size:14px;color:#5a5f6a;margin:3px 0 0;}
.two{display:flex;gap:44px;}
.two>div{flex:1;}
.ask{font-size:clamp(17px,2.2vw,25px);font-weight:700;line-height:1.3;margin:0 0 12px;}
.vis{background:var(--a);color:#fff;border-left:none;}
.vis b{color:#fff;}
.foot{position:absolute;bottom:5.2%;left:6.2%;right:6.2%;display:flex;justify-content:space-between;font:12px/1 ui-monospace,monospace;color:#9098a3;letter-spacing:.04em;}
.bar{position:fixed;left:0;bottom:0;height:4px;width:100%;background:rgba(0,0,0,.08);z-index:9;}
.bar i{display:block;height:100%;width:0;background:var(--a);transition:width .2s;}
.hint{position:fixed;right:14px;top:12px;font:11px/1 ui-monospace,monospace;color:#8b929d;letter-spacing:.05em;}
@media print{
  @page{size:landscape;margin:0;}
  body{background:#fff;}
  .deck{display:block;}
  .slide{display:flex!important;flex-direction:column;justify-content:center;width:100vw;height:100vh;aspect-ratio:auto;border-radius:0;box-shadow:none;page-break-after:always;}
  .bar,.hint{display:none;}
}
"""

_DECK_JS = """
var S=[].slice.call(document.querySelectorAll('.slide')),i=0,bar=document.querySelector('.bar i');
function show(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach(function(s,k){s.classList.toggle('active',k===i);});if(bar)bar.style.width=((i+1)/S.length*100)+'%';}
document.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(i+1);}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(i-1);}});
document.addEventListener('click',function(e){if(e.target.closest('a'))return;show(e.clientX>window.innerWidth/2?i+1:i-1);});
show(0);
"""


def _render_deck(d: dict) -> str:
    accent = _esc(d.get("accent") or "#8C1515")
    company = _esc(d.get("company") or "Company")
    one = _esc(d.get("one_liner") or "")
    tag = _esc(d.get("tagline") or "")
    pr = d.get("problem") or {}
    so = d.get("solution") or {}
    mk = d.get("market") or {}
    bm = d.get("business_model") or {}
    tr = d.get("traction") or {}
    mo = d.get("moat") or {}
    tm = d.get("team") or {}
    ak = d.get("ask") or {}
    vision = _esc(d.get("vision") or "")

    def slide(inner, label, n):
        lab = '<div class="lab">%s</div>' % _esc(label) if label else ""
        foot = ('<div class="foot"><span>%s</span><span>%d / 6</span></div>'
                % (company, n))
        return '<section class="slide">%s<div class="body">%s</div>%s</section>' % (lab, inner, foot)

    s1 = slide(
        '<div class="kicker">Pitch · Techstars format</div>'
        '<h1 class="co">%s</h1><p class="one">%s</p>%s' % (
            company, one, ('<p class="tag">%s</p>' % tag) if tag else ""),
        "", 1)

    s2 = slide(
        '<h2>%s</h2><ul>%s</ul>%s' % (
            _esc(pr.get("headline", "")), _lis(pr.get("points")),
            ('<div class="call"><b>Why now.</b> %s</div>' % _esc(pr.get("why_now"))) if pr.get("why_now") else ""),
        "01 · Problem · feel the pain", 2)

    s3 = slide(
        '<h2>%s</h2><ol>%s</ol>%s' % (
            _esc(so.get("headline", "")), _lis(so.get("how")),
            ('<div class="call"><b>The aha.</b> %s</div>' % _esc(so.get("aha"))) if so.get("aha") else ""),
        "02 · Solution · show, do not tell", 3)

    nums = ""
    for k, lab in (("tam", "TAM"), ("sam", "SAM"), ("som", "SOM")):
        if mk.get(k):
            nums += '<div class="num"><div class="nlab">%s</div><div class="nval">%s</div></div>' % (lab, _esc(mk.get(k)))
    s4 = slide(
        '<h2>Market and business model</h2><div class="nums">%s</div>%s'
        '<div class="call"><b>%s</b><ul>%s</ul></div>' % (
            nums,
            ('<p class="note">%s</p>' % _esc(mk.get("note"))) if mk.get("note") else "",
            _esc(bm.get("headline", "How it makes money.")), _lis(bm.get("streams"))),
        "03 · Market and model · size and money", 4)

    s5 = slide(
        '<div class="two"><div><div class="h3">%s</div><ul>%s</ul></div>'
        '<div><div class="h3">%s</div><ul>%s</ul></div></div>' % (
            _esc(tr.get("headline", "Traction")), _lis(tr.get("proof")),
            _esc(mo.get("headline", "Why we win")), _lis(mo.get("why_you_win"))),
        "04 · Traction and moat · proof and why you win", 5)

    s6 = slide(
        '<div class="two"><div><div class="h3">%s</div><ul>%s</ul></div>'
        '<div><div class="h3">The ask</div><p class="ask">%s</p><ul>%s</ul></div></div>%s' % (
            _esc(tm.get("headline", "Team")), _lis(tm.get("members")),
            _esc(ak.get("ask", "")), _lis(ak.get("use_of_funds")),
            ('<div class="call vis"><b>The dream.</b> %s</div>' % vision) if vision else ""),
        "05 · Team and the ask · faces, be specific, the dream", 6)

    css = _DECK_CSS.replace("__ACCENT__", accent)
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s · pitch</title><style>%s</style></head><body>"
            "<div class=\"hint\">arrow keys, or click, to move · print to PDF</div>"
            "<div class=\"deck\">%s%s%s%s%s%s</div>"
            "<div class=\"bar\"><i></i></div><script>%s</script></body></html>"
            % (company, css, s1, s2, s3, s4, s5, s6, _DECK_JS))


@mcp.tool()
def deck_outline() -> str:
    """The Techstars pitch format, distilled to 6 slides, plus the exact JSON
    schema to fill and pass to pitch_deck(). Every slide must answer 'so what?'.
    Fill one company's story into the schema, then call pitch_deck to render the
    self-contained HTML deck. Start here before making a deck."""
    return _j({
        "format": TECHSTARS_DECK,
        "deck_json_schema": {
            "company": "string", "one_liner": "string, the elevator pitch",
            "tagline": "string, optional",
            "accent": "hex color, optional, default #8C1515",
            "problem": {"headline": "string", "points": ["string"], "why_now": "string"},
            "solution": {"headline": "string", "how": ["string, about three steps"], "aha": "string"},
            "market": {"tam": "string", "sam": "string", "som": "string", "note": "string"},
            "business_model": {"headline": "string", "streams": ["string"]},
            "traction": {"headline": "string", "proof": ["string"]},
            "moat": {"headline": "string", "why_you_win": ["string"]},
            "team": {"headline": "string", "members": ["string"]},
            "ask": {"headline": "string", "ask": "string", "use_of_funds": ["string"]},
            "vision": "string, the dream if it works",
        },
        "example": DECK_SCHEMA_EXAMPLE,
        "then": "pitch_deck(name, deck_json)  writes the .html deck to disk.",
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def pitch_deck(name: str, deck_json: str, out_path: str = "") -> str:
    """Deliver a self-contained HTML pitch deck for one company: 6 slides in the
    Techstars format (cover, problem, solution, market and model, traction and
    moat, team and the ask). Pass deck_json as a JSON object following the schema
    from deck_outline(). The deck is written to disk as an .html file you open in
    a browser (arrow keys or click to navigate, print to PDF for a handout).
    Returns the saved path. Call deck_outline() first for the fields to fill."""
    try:
        d = json.loads(deck_json)
        if not isinstance(d, dict):
            raise ValueError("deck_json must be a JSON object")
    except (json.JSONDecodeError, ValueError) as e:
        return _j({"error": "Could not parse deck_json: %s" % e,
                   "hint": "Call deck_outline() for the schema and an example."})
    d.setdefault("company", name)
    html = _render_deck(d)
    path = out_path.strip() or os.path.join(os.getcwd(), "%s_pitch.html" % _slug(d.get("company", name)))
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
    except OSError as e:
        return _j({"error": "Could not write file: %s" % e, "html_length": len(html)})
    return _j({
        "company": d.get("company", name),
        "slides": 6,
        "format": "Techstars, distilled to 6 slides",
        "saved_to": path,
        "open": "Open the file in a browser. Arrow keys or click to move. Print to PDF for a one page per slide handout.",
        "disclaimer": DISCLAIMER,
    })

if __name__ == "__main__":
    mcp.run()
