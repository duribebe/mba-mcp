# MBA Company Analyzer (`mba-mcp`)

> *"La empresa es la sombra alargada del CEO."*
> The company is the elongated shadow of the CEO.
> **Carlos Llano Cifuentes, founder of IPADE Business School**

A pocket business school as an [MCP](https://modelcontextprotocol.io) server for Claude. It gives Claude the Harvard and IPADE case canon as structured frameworks, scoring rubrics, and comparison scaffolds, so a student can analyze and compare three or more companies (real or invented) and then face the deepest question of the age of AI:

**When a machine can do most of the work, would you still be inspired enough to build it for the next ten years?**

Viability is becoming cheap and abundant. Motivation is scarce. This tool ranks companies by the head and helps you decide with the whole person.

---

## What it does

You point Claude at three or more companies. For each one, the analyzer supplies the questions; Claude supplies the reasoning. Then it scores, compares, and pushes you to the founder's real question.

**Frameworks it teaches**

1. **The Value Triangle**: the three kinds of value a customer receives, utility, monetary, and psychological.
2. **Value Capture** (pricing): the value stick (willingness to pay minus cost), and the three ways to set price.
3. **Values**: what the company actually stands for, judged by its choices, not its slogans.
4. **Sustainability**: business durability, and whether it renews or depletes the world it uses.
5. **Founder Fit and Motivation**: why you, why now, philosophical alignment, and the ten year test.
6. **The Future of Work**: what stays irreplaceably human when AI can do the execution.
7. **The Pitch** (Techstars): the minimal elements a pitch must have, in order, closed by one rule, every slide answers "so what?".
8. **The case method**: situation (customer and market), alternatives (value triangle and value capture), financials (the 3 R's).

**How it scores.** Grade each of the eight lenses from **1 to 4** (1 weak, 2 fair, 3 strong, 4 exceptional). The overall grade is the average, on the same 1 to 4 scale. Simple on purpose.

| Lens | Grade 1 to 4 |
| --- | --- |
| Customer and Market | 1 to 4 |
| Value Creation (value triangle) | 1 to 4 |
| Value Capture (pricing) | 1 to 4 |
| Competition and Moat | 1 to 4 |
| Founder Fit and Motivation | 1 to 4 |
| Values and Ethics | 1 to 4 |
| Sustainability and Durability | 1 to 4 |
| AI-Resilience (future of work) | 1 to 4 |

Grade 3 or higher is compelling, 2.4 or higher is promising, 1.8 or higher is viable but thin, below that is not yet.

## The tools

| Tool | What it does |
| --- | --- |
| `status` | What the analyzer is and the run flow. Start here. |
| `list_frameworks` | Index of the frameworks. |
| `get_framework(name)` | Open one framework in full. |
| `analyze_company(name, description)` | The lens by lens scaffold, plus the bull case, bear case, key metric, and confidence. |
| `score_company(name, scores_json)` | The 1 to 4 scorecard and verdict. |
| `compare_companies(companies_json)` | One comparison matrix and ranking. |
| `motivation_check(name)` | The ten year test. |
| `future_of_work(name)` | What stays human when AI does the rest. |
| `deck_outline()` | The Techstars pitch format, distilled to 6 slides, and the deck JSON schema. |
| `pitch_deck(name, deck_json)` | Delivers a self-contained Techstars HTML pitch deck (6 slides) written to disk. |
| `carlos_llano_principle()` | The founding principle, with translation. |
| `get_exercise()` | The full student exercise. |
| `rebut(position)` | Adversarial investor objections to a claim. |

## The pitch deck

Once a company is analyzed, the analyzer can deliver a real pitch deck, not just a critique. Call `deck_outline()` to see the Techstars format (Problem, Solution, Market, Business Model, Traction, Team, The Ask, Vision) distilled to 6 slides, fill the company's story into the JSON schema, then call `pitch_deck(name, deck_json)`. It writes a self-contained `.html` deck you open in a browser (arrow keys or click to move, print to PDF for a handout). Every slide answers the Techstars question, "so what?"

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/duribebe/mba-mcp.git
cd mba-mcp
pip install -r requirements.txt   # installs the mcp SDK
```

## Connect it to Claude

**Claude Code** (one line):

```bash
claude mcp add mba -- python /absolute/path/to/mba-mcp/server.py
```

**Claude Desktop**: add this to `claude_desktop_config.json` (Settings, Developer, Edit Config), then restart Claude:

```json
{
  "mcpServers": {
    "mba": {
      "command": "python",
      "args": ["/absolute/path/to/mba-mcp/server.py"]
    }
  }
}
```

Use the full path to a Python that has the `mcp` package installed. Then, in a chat, just ask Claude to "use the MBA analyzer to compare Netflix, a lemonade stand, and my app idea."

## The exercise

The classroom exercise is in [`EXERCISE.md`](EXERCISE.md) and is also returned by the `get_exercise` tool. In short: pick three companies, analyze and score each, compare them on one matrix, run the future of work lens, and then answer honestly whether you would be inspired to build the one you would build for the next ten years. Decide, and defend it with the frameworks.

## Why this exists

Most of the tasks inside a company are becoming things AI can do. The one input it cannot supply for you is the motivation to start, and to keep going through the hard middle. A company will always be the elongated shadow of the person who leads it. So before you ask whether a business is viable, ask whether it is a shadow you would be proud to cast.

## License

MIT. See [`LICENSE`](LICENSE). Built by Daniel Uribe, GenoBank.io, 2026.
