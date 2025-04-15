DAO Voting Pattern Analyzer 🗳️
This project analyzes DAO voting trends across the Aptos blockchain. It includes a visually rich dashboard built with Dash and a landing website built by teammates that introduces the project and routes users to the dashboard.

🔗 Live Link
📊 Dashboard: [Explore the Full Dashboard][https://dao-voting-dashboard-azwk.onrender.com]
(Please wait for couple of minutes after clicking of "fetch Aptos data" since it takes few minutes fetch the data and visualise it)

🧩 Project Structure
🖥️ Landing Website (Local Project by Teammates)
A static frontend website created using HTML, CSS, and JavaScript. Though not deployed, this website serves as a visual overview of the project with:

📝 About section
✨ Feature highlights like:
Proposal Calendar
Blockchain Integration
Global Impact
🚀 Button to open the full dashboard (when hosted locally)
This site was created as part of the project to improve user experience and guide users into the analytical dashboard.

📊 DAO Voting Dashboard (Dash App)
A Python Dash-based dashboard that fetches and visualizes DAO data from the Aptos blockchain. It includes:

DAO-specific proposal history
Voter participation analytics
Visualizations (bar graphs, pie charts) for trend analysis
Dashboard navigation through dropdowns and filters
🔍 Features Summary
Feature	Description
📅 Proposal Calendar	View upcoming and past proposal data
🔐 Blockchain Insights	Uses Aptos API for transparency in DAO governance
🌍 Global Impact	Understand how DAOs influence decentralized decisions
📊 Visual Analytics	Clean charts and graphs built using Plotly Dash
🛠 Tech Stack
Landing Website: HTML, CSS, JavaScript (local only)
Dashboard: Python, Dash, Plotly
Blockchain: Aptos API
Deployment: Render
Version Control: Git & GitHub
🧠 How It Works
Connects to Aptos API to fetch DAO-related proposal and voting data
Visualizes data with graphs and filters in the dashboard
(Locally) integrates with a landing page that provides an overview
🖼️ Screenshots
Dashboard View
Data fetched by Aptos:
Screenshot 2025-04-13 164757 Screenshot 2025-04-13 164811

When you give your own csv file:
Screenshot 2025-04-13 165023 Screenshot 2025-04-13 165014 Screenshot 2025-04-13 164958

Landing Website (Local)
Screenshot 2025-04-13 165526 Screenshot 2025-04-13 165614 Screenshot 2025-04-13 165557 Screenshot 2025-04-13 165541

🧪 Run Dashboard Locally
git clone https://github.com/lokitha-muni/dao-voting-dashboard.git
cd dao-voting-dashboard
pip install -r requirements.txt
python app2.py
