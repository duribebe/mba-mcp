# Worked example: comparing three companies

A short walkthrough so you can see the shape of the output. Here three companies are compared: a real venture (GenoBank.io), an invented student project (a fictional face licensing app called FaceVault), and a deliberately weak idea (a thin wrapper around someone else's AI model). The scores below are illustrative, to show the mechanics, not a valuation of any real firm.

### Step 1 and 2. Analyze and score each

Each company was run through `analyze_company`, then scored 0 to 10 on the eight dimensions with `score_company`.

### Step 3. Compare (`compare_companies`)

| Dimension | Weight | GenoBank.io | FaceVault | AI wrapper | Leader |
| --- | --- | --- | --- | --- | --- |
| Customer and Market | 15 | 8 | 7 | 6 | GenoBank.io |
| Value Creation | 15 | 8 | 7 | 5 | GenoBank.io |
| Value Capture | 15 | 6 | 5 | 4 | GenoBank.io |
| Competition and Moat | 12 | 8 | 6 | 2 | GenoBank.io |
| Values and Ethics | 10 | 9 | 9 | 6 | tie |
| Sustainability | 10 | 8 | 7 | 4 | GenoBank.io |
| Founder Fit and Motivation | 13 | 9 | 9 | 5 | tie |
| AI-Resilience | 10 | 8 | 8 | 2 | tie |

**Ranking:** GenoBank.io 79.3 (compelling), FaceVault 71.4 (promising), AI wrapper 43.4 (not yet).

Read the story in the numbers. The AI wrapper is not evil, but it has no moat and almost no AI-resilience. When the underlying model gets cheaper or the platform copies the feature, the wrapper collapses. That is the lesson.

### Step 4. Future of work (`future_of_work`)

Split each company's work into two piles. For the AI wrapper, nearly everything lands in the "AI can do this soon" pile, which is why it scored a 2. For GenoBank.io and FaceVault, the human core is trust, consent, and the founder's mission, which AI can assist but not replace.

### Step 5. The real question (`motivation_check`)

The two strong companies tie on viability. The tie breaks on the founder. FaceVault was built by a seventeen year old who could not stop thinking about who owns her face. That is a shadow she would be proud to cast. Numbers rank viability. Motivation decides.

### Step 6. Decide and defend

> "I would build FaceVault. On the matrix it trails GenoBank.io only on scale and moat, both of which grow with time. It wins where it matters to me: it is the problem I obsess over, the timing is right as AI makes deepfakes trivial, and it aligns with who I want to become. It is a shadow I would be proud to cast."
