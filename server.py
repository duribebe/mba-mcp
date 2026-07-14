"""
MBA Company Analyzer, an MCP server for the Claude / Anthropic framework.

A pocket business school. It gives Claude the Harvard and IPADE case canon as
structured frameworks, scoring rubrics, and comparison scaffolds, so a student
can analyze and compare three or more companies (real or invented) and then face
the deepest question of the age of AI: when a machine can do most of the work,
would you still be motivated enough to get up from bed and build it?

Grounded in the IPADE 4 C's, the value triangle, value based pricing, and the
principle of IPADE founder Carlos Llano Cifuentes: "La empresa es la sombra
alargada del CEO." The company is the long shadow of the CEO.

Run: python3 server.py   (stdio transport)
"""
import json  # noqa: E402
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
    "translation_en": "The company is the long shadow of the CEO.",
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
    "fourcs": {
        "title": "The 4 C's (IPADE strategic diagnostic)",
        "definition": (
            "Read any company as four forces you must understand before you "
            "act. The 4 C's diagnose the situation. The 4 P's (Producto, "
            "Precio, Plaza, Promocion) are the actions you take in response. "
            "IPADE sometimes adds Canales (channels) and Comunidad (community "
            "and social responsibility) as a fifth C."
        ),
        "parts": {
            "Compania (Company)": (
                "The firm itself: its mission, resources, capabilities, and "
                "its Strengths, Weaknesses, Opportunities, and Threats (SWOT). "
                "Ask: what does this company have that rivals cannot easily "
                "copy?"
            ),
            "Consumidor (Customer)": (
                "Who is really the customer, read through the Decision Making "
                "Unit (DMU): the user, the beneficiary, the payer, the "
                "decider, the influencer, and the evaluator. These are often "
                "different people. Ask: whose problem is this, who pays, who "
                "decides, and how strong is their willingness to pay?"
            ),
            "Competencia (Competition)": (
                "Rivals, substitutes, and new entrants. Positioning equals the "
                "segment you choose plus your differentiation. Ask: why would "
                "a customer pick this over the alternatives, and can that edge "
                "be defended (the moat)?"
            ),
            "Contexto (Context)": (
                "The macro environment: technology, regulation, economy, "
                "society, and culture. This is where 'why now' lives. Ask: "
                "what just changed in the world that makes this possible or "
                "urgent today?"
            ),
        },
        "scores": "customer_market, competition_moat, contexto (why now)",
    },
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
            "Carlos Llano's principle bites: the company is the long shadow of "
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
        "title": "Founder Fit and Motivation: would you get up from bed for this?",
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
            "Energy (the get up from bed test)": (
                "Would you get out of bed for this for years, through the hard "
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
    "case_method": {
        "title": "The IPADE case method: how to run the whole analysis",
        "definition": "Do not rush to a verdict. Diagnose, then decide, then defend.",
        "parts": {
            "1. Situation": "Read the 4 C's (and the 5 C's) to find the real problem.",
            "2. Alternatives": (
                "Use the 4 P's (Producto, Precio, Plaza, Promocion) to design "
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
    "4cs": "fourcs", "4 c": "fourcs", "4 c's": "fourcs", "four cs": "fourcs",
    "fourc": "fourcs", "cs": "fourcs", "c": "fourcs",
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
}

DIMENSIONS = [
    {"key": "customer_market", "label": "Customer and Market (4 C's)", "weight": 15},
    {"key": "value_creation", "label": "Value Creation (value triangle)", "weight": 15},
    {"key": "value_capture", "label": "Value Capture (pricing)", "weight": 15},
    {"key": "competition_moat", "label": "Competition and Moat", "weight": 12},
    {"key": "values_ethics", "label": "Values and Ethics", "weight": 10},
    {"key": "sustainability", "label": "Sustainability and Durability", "weight": 10},
    {"key": "founder_motivation", "label": "Founder Fit and Motivation", "weight": 13},
    {"key": "ai_resilience", "label": "AI-Resilience (future of work)", "weight": 10},
]
def _verdict(total: float) -> str:
    if total >= 75:
        return "Compelling. This is worth building, and worth building by you."
    if total >= 60:
        return ("Promising. The idea is real. Sharpen the weakest C's and the "
                "moat before you commit.")
    if total >= 45:
        return ("Viable but thin. The business could exist, but the edge or "
                "the motivation is weak. Rework it, or pick a different shadow "
                "to cast.")
    return ("Not yet. Fix the fundamentals, or choose a company you would "
            "actually get up from bed for.")


def _score_one(scores: dict):
    """Return (total_0_100, per_dimension_list, missing_keys)."""
    per = []
    used_weight = 0.0
    got = 0.0
    missing = []
    for d in DIMENSIONS:
        k = d["key"]
        if k in scores and scores[k] is not None:
            try:
                v = float(scores[k])
            except (TypeError, ValueError):
                v = 0.0
            v = max(0.0, min(10.0, v))
            contrib = (v / 10.0) * d["weight"]
            got += contrib
            used_weight += d["weight"]
            per.append({"dimension": d["label"], "key": k, "score": round(v, 1),
                        "weight": d["weight"], "contribution": round(contrib, 1)})
        else:
            missing.append(k)
            per.append({"dimension": d["label"], "key": k, "score": None,
                        "weight": d["weight"], "contribution": 0.0})
    # Normalize to 0..100 over the weights actually provided, so partial scoring
    # is not unfairly penalized. If nothing was scored, total is 0.
    total = round((got / used_weight) * 100, 1) if used_weight else 0.0
    return total, per, missing


EXERCISE = """MBA COMPANY ANALYZER, THE STUDENT EXERCISE

Objective. Practice thinking like a founder and an investor, then discover the
one input AI cannot supply for you.

Step 1. Pick three companies. At least one real and one you invent. A strong
set is one giant, one startup, and your own idea.

Step 2. Analyze each with the tool. For each company run analyze_company, answer
the questions it returns for the 4 C's, the value triangle, value capture,
values, and sustainability, then record a score from 0 to 10 on each of the
eight dimensions with score_company.

Step 3. Compare. Run compare_companies with all three scorecards. Read the
matrix. Which company wins on customer and market, on value capture, on moat?
Which is only cheap, or only clever?

Step 4. The future of work. Run future_of_work on each. Split the work into what
an AI could do tomorrow and what still needs a motivated human. Notice that the
most durable companies keep a large, human core.

Step 5. The real question. Run motivation_check on the company you would build.
Answer honestly: why you, why now, does it align with who you want to become,
and would you get up from bed for it for years. The numbers rank viability.
This ranks you.

Step 6. Decide and defend. In one paragraph, name the company you would build
and defend the choice with the frameworks. Remember Carlos Llano: the company is
the long shadow of the CEO. Choose a shadow you are proud to cast.
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
        "grounding": ("Harvard and IPADE case method. The 4 C's and 4 P's, the "
                      "value triangle, value based pricing, and Carlos Llano's "
                      "principle of the long shadow of the CEO."),
        "epigraph": CARLOS_LLANO,
        "how_to_use": [
            "1. get_framework to learn any lens (or list_frameworks for the index).",
            "2. analyze_company(name, description) for each company to get the scaffold.",
            "3. score_company(name, scores_json) to record 0 to 10 on the eight dimensions.",
            "4. compare_companies(companies_json) to rank them on one matrix.",
            "5. future_of_work(name) to see what stays human when AI does the rest.",
            "6. motivation_check(name) for the get up from bed test on the one you would build.",
            "7. get_exercise for the full classroom exercise.",
        ],
        "dimensions": [{"key": d["key"], "label": d["label"], "weight": d["weight"]}
                       for d in DIMENSIONS],
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def list_frameworks() -> str:
    """List the analytical frameworks available, each with a one line summary.
    Use get_framework(name) to open any of them."""
    return _j({
        "frameworks": [{"key": k, "title": v["title"]} for k, v in FRAMEWORKS.items()],
        "tip": "get_framework('fourcs' | 'value_triangle' | 'value_capture' | "
               "'values' | 'sustainability' | 'motivation' | 'future_of_work' | "
               "'case_method'), or empty for all.",
    })


@mcp.tool()
def get_framework(name: str = "") -> str:
    """Open one analytical framework in full: its definition, its parts, the
    questions to ask, and which scoring dimension it feeds. Pass a key such as
    'fourcs', 'value_triangle', 'value_capture', 'values', 'sustainability',
    'motivation', 'future_of_work', or 'case_method'. Aliases like '4 c's',
    'pricing', 'why you', or 'ai' also work. Pass an empty string for all."""
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
    across every framework, plus a blank 0 to 10 scoring template. This tool
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
            "Answer each lens below specifically for this company, using what "
            "you know or can reasonably infer. Be concrete. Then assign a score "
            "from 0 to 10 on each dimension and pass them to score_company. Do "
            "not invent precise financials you do not have; reason from the "
            "business model and hedge honestly."
        ),
        "lenses": lenses,
        "scoring_template": {d["key"]: None for d in DIMENSIONS},
        "scoring_guide": {d["key"]: d["label"] for d in DIMENSIONS},
        "next": "score_company(name, scores_json)  then  compare_companies(companies_json)",
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def score_company(name: str, scores_json: str) -> str:
    """Record a company's scorecard and get a weighted total and a verdict.
    Pass scores_json as a JSON object mapping dimension keys to numbers from 0
    to 10, for example: {"customer_market": 8, "value_creation": 7,
    "value_capture": 6, "competition_moat": 5, "values_ethics": 9,
    "sustainability": 7, "founder_motivation": 9, "ai_resilience": 8}. Missing
    dimensions are allowed and are normalized out of the total."""
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
        "total_0_to_100": total,
        "verdict": _verdict(total),
        "per_dimension": per,
        "missing_dimensions": missing,
        "note": ("The total ranks viability. It does not decide motivation. Run "
                 "motivation_check before you commit."),
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def compare_companies(companies_json: str) -> str:
    """Compare two to four scored companies on one matrix. Pass companies_json
    as a JSON array of objects, each with a name and a scores object, for
    example: [{"name":"A","scores":{"customer_market":8,...}}, {"name":"B",
    "scores":{...}}]. Returns a dimension by company matrix, the leader on each
    dimension, the overall ranking, and a decision scaffold."""
    try:
        companies = json.loads(companies_json)
        if not isinstance(companies, list) or not companies:
            raise ValueError("companies_json must be a non empty JSON array")
    except (json.JSONDecodeError, ValueError) as e:
        return _j({"error": f"Could not parse companies_json: {e}",
                   "expected": '[{"name":"A","scores":{"customer_market":8,...}}, ...]'})
    computed = []
    for c in companies[:4]:
        nm = c.get("name", "Company")
        total, per, _ = _score_one(c.get("scores", {}))
        computed.append({"name": nm, "total": total,
                         "scores": {p["key"]: p["score"] for p in per}})
    names = [c["name"] for c in computed]
    matrix = []
    for d in DIMENSIONS:
        row = {"dimension": d["label"], "weight": d["weight"]}
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
        "ranking": [{"rank": i + 1, "name": c["name"], "total_0_to_100": c["total"],
                     "verdict": _verdict(c["total"])}
                    for i, c in enumerate(ranking)],
        "decision_scaffold": (
            "The ranking measures viability, not destiny. Two moves finish the "
            "analysis. First, if the top two are close, break the tie with the "
            "future of work: which one keeps the larger human core when AI "
            "commoditizes execution. Second, override the numbers with the get "
            "up from bed test: among the viable companies, which one would you "
            "be truly motivated to build, for years, through the hard middle? "
            "Why you? Why now? Carlos Llano: the company is the long shadow of "
            "the CEO. Rank by the head, decide with the whole person."
        ),
        "epigraph": CARLOS_LLANO,
        "disclaimer": DISCLAIMER,
    })


@mcp.tool()
def motivation_check(name: str) -> str:
    """The get up from bed test for the company you would actually build. Returns
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
            "energy": fw["parts"]["Energy (the get up from bed test)"],
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
    the get up from bed test. Hand this to a class, or run it yourself."""
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
            "a spreadsheet that no one will get up from bed for?",
        ],
        "instruction": ("Voice the single toughest objection above in the voice "
                        "of a skeptical investor, then say what evidence would "
                        "actually answer it."),
        "disclaimer": DISCLAIMER,
    })


if __name__ == "__main__":
    mcp.run()
