# StrongTies – A Networking Insights Tool
**Find the people in your network who can open doors — and the ones you can help in return.**

StrongTies is a **noncommercial, source-available application** that gives job seekers and professionals insight into their LinkedIn connection network. By importing your connections (names, companies, and positions only; no emails or messages), the tool builds a social graph of your first- and second-degree contacts and uses network-analysis methods to identify:

- Which of your direct contacts are positioned to introduce you to your target companies  
- Which of your second-degree contacts are within reach via warm introductions  
- How clusters of connections overlap to create stronger paths for outreach  

Networking becomes less about hoping and more about strategy. With StrongTies you get actionable insight into who to connect with — and how to do it in a way that supports your goals, while honoring your network.

---

## Features

### Currently Available
- **Local Data Analysis:** Upload your LinkedIn-style CSV files (names, companies, positions only) and analyze your connections directly in your browser.  
- **Privacy-Preserving:** All processing happens locally; no data is uploaded or shared externally.  
- **User-Friendly Interface:** Streamlit-powered app with a clean, modern design for easy data upload and exploration.  
- **Connection Overview:** Instantly view and explore your imported connections in a sortable, filterable table.  
- **Identifier Selection:** Analyze your network by selecting your user identifier from uploaded files.  
- **Error Handling:** Clear feedback for successful uploads and helpful error messages for issues.

### Coming Soon
- **Network Graph Construction:** Visualize your professional social graph, showing how you and your contacts are connected.  
- **Advanced Metrics:** Centrality measures (betweenness, closeness, etc.) and community detection to highlight key connectors and clusters.  
- **Introduction Path Analysis:** Discover optimal paths for warm introductions to second-degree contacts and target companies.  
- **Visual Insights:** Interactive network diagrams and cluster visualizations.  
- **Group Collaboration:** Combine multiple users' networks for richer analysis and mutual support.  
- **Exportable Reports:** Download ranked lists of connectors and suggested introduction paths.  
- **Expanded Documentation:** In-app help, privacy details, and ethical guidelines.

---

## Why StrongTies Matters
Traditional networking advice often leaves you asking: "Who should I reach out to? Through whom?" StrongTies takes the guesswork out of that process. Based on social-network theory and real data, it highlights where opportunity lives in your network, so you can spend time where it counts.

---

## How It Works
1. **Export Connection Data** – Export your LinkedIn connections, providing name, company, and position fields only.  
   [See LinkedIn’s instructions for exporting your connections.](https://www.linkedin.com/help/linkedin/answer/a566336/export-connections-from-linkedin)
2. **Graph Construction** – StrongTies builds a network graph: people are vertices; relationships are edges.  
3. **Analysis Metrics** – The tool calculates centrality measures (e.g., betweenness, closeness) and community structure to detect strong introduction paths.  
4. **Insight Output** – You receive a ranked list of high-potential connections and optional visualizations of your network.  

> _All processing happens locally or via open-source code; no sensitive data is shared._

---

## User Guide

For detailed instructions, ethical principles, and best practices, please see the [StrongTies User Guide](./user-guide.md).

---

## Get Involved
We’re seeking contributors, testers, and volunteer pairs to pilot StrongTies:  
- You have a LinkedIn connection export and are open to mapping your network.  
- You’re looking for your next opportunity (or supporting someone who is).  
- You’re willing to provide feedback on the tool’s usability and results.

To join, create an issue or pull request here on GitHub, or reach out via `strongties.networking@gmail.com`. Let’s build a tool that makes networking clearer, fairer, and more human.

---

## License
StrongTies is licensed under the [Polyform Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/).

> You may use, copy, modify, and share StrongTies **for noncommercial purposes only**.  
> For commercial use or integration, please contact the author for a separate license.  
> All copies must include this license notice.

---

*StrongTies is free, noncommercial, and built on the belief that the best networks are built on reciprocity, insight, and intention.*