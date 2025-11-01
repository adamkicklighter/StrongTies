# 🧭 GitHub Copilot Instructions for StrongTies

## Project Intent
**StrongTies** is a noncommercial, open project designed to help professionals better understand their *existing* career networks.  
It analyzes exported LinkedIn-style data (names, companies, positions only) to:
- Visualize the structure of a professional’s first- and second-degree network,
- Identify high-potential introduction paths,
- Highlight strong clusters of opportunity for outreach.

The goal is *insight*, not exploitation. The application should **respect privacy**, **never share data externally**, and **operate locally**.

---

## Core Objectives for Copilot
When generating code, prioritize:
1. **Data Ethics:** Never collect, upload, or infer sensitive data beyond what’s provided in CSVs.
2. **Local Processing:** All analysis and visualizations run on the user’s local environment.
3. **Transparency:** Generated code should be easy to inspect, explain, and reproduce.
4. **Modularity:** Encourage reusable, well-documented modules under `src/` (e.g. `data_loader`, `graph_builder`, `network_metrics`).
5. **Clarity:** Generate clear function names, docstrings, and type hints.
6. **Privacy by Design:** If unsure whether a feature might expose or leak data, default to safety.

---

## Data Schema
Input CSVs include:
- `connections.csv`:  
  - `First Name`: First name of the connection  
  - `Last Name`: Last name of the connection  
  - `Company`: Current company of the connection  
  - `Position`: Current position/title of the connection

No emails, messages, or unique identifiers.  
Synthetic sample data for testing lives in `data/`.

Copilot should not suggest collecting data from LinkedIn APIs or web scraping — the system is *user-provided data only*.

---

## Desired Outputs
Copilot should help produce:
- Ranked lists of **key connectors** and **introduction paths**.
- Optional **network visualizations** using `matplotlib` or `Plotly`.
- CSV summaries written to `results/reports/`.

All output files must be **local** (no uploads).

---

## Technical Stack

### Preferred (primary)
These are the libraries and tools we primarily use and test against. When possible, prefer these for consistency across the repo:

- **pandas** for data handling  
- **networkx** for graph construction and analysis  
- **matplotlib** for simple visualizations (or **plotly** when interactive plots are warranted)  
- **faker** for generating synthetic data  
- **pytest** for testing

### Secondary / Acceptable alternatives
Alternative open-source libraries that are acceptable when they meaningfully improve clarity, performance, or developer experience:

- **plotly**, **altair**, **matplotlib** (interactive vs static choices)
- **igraph** or **python-igraph** for large-graph performance
- **polars** or **dask** for high-performance or out-of-core tabular processing
- **numpy**, **scipy** for numerical routines

### Openness policy
We prefer the tools above for maintainability and reproducibility, but the project is **not restricted** to them. Copilot and contributors are **encouraged** to propose and use other open-source, locally-executable technologies when they:
- improve correctness, performance, or usability;
- remain consistent with the project’s noncommercial and privacy-first constraints; and
- are documented and tested (add rationale in PRs and update `docs/`).

> Note: Avoid introducing cloud-only, closed-source, or data-exfiltration dependencies without an explicit maintainer-approved design and documentation.

---

## Repository Organization
src/ → core logic modules
data/ → sample CSVs and synthetic generation scripts
notebooks/ → exploratory Jupyter notebooks
results/ → analysis outputs
docs/ → documentation, architecture, and privacy notes


---

## Licensing
StrongTies uses the **Polyform Noncommercial 1.0.0 License**.
Copilot must assume:
- Generated code is intended for **noncommercial** use.
- Any code snippets must remain consistent with this licensing restriction.

---

## Tone and Style of Code
When generating code or docstrings:
- Be **professional**, **educational**, and **ethical**.
- Write in a clear, instructive tone.
- Include context where needed (docstrings, comments, type hints).

Example guidance:
> “StrongTies analyzes user-provided CSV files to construct a social graph and identify potential professional introductions.”

---

## Explicit Boundaries
Copilot **must not**:
- Suggest code that accesses or scrapes LinkedIn, social media, or web data.
- Store or transmit user data to any external service.
- Generate marketing, recruitment, or surveillance-oriented functionality.
- Reuse code with unknown licensing terms.

---

## Example Goal for Copilot
When the user provides two CSVs of connection data, Copilot should help build:
1. A **graph** of relationships between people and companies.
2. **Network metrics** such as betweenness or closeness centrality.
3. **Visual or tabular summaries** identifying likely introduction paths.

---

*This file defines the ethical and practical context for GitHub Copilot’s assistance within the StrongTies project.  
All code generation should reflect these values of privacy, transparency, and reciprocity.*