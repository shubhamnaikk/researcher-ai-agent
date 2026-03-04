# 🧠 Intelligence Terminal: Agentic Researcher Lab

Intelligence Terminal is a high-end, premium AI research application that doesn't just "write"—it **validates**. Using a recursive agentic loop, it synthesizes deep-dive research briefs and then subjects them to a rigorous secondary validation audit to ensure factual accuracy and objective analysis.

![Terminal View](file:///Users/shubhamnaik/.gemini/antigravity/brain/4d7a6b4b-e4b9-4025-97f2-397388321e4a/initial_app_view_1772590878415.png)

## ⚡ The Agentic Loop
Unlike standard LLM interfaces, this terminal utilizes a multi-node pipeline:
1. **Researcher Node**: Synthesizes a comprehensive analysis brief from multiple perspectives.
2. **Auditor Node**: Recursively fact-checks the brief, identifying biases and hallucinations.

## 🎨 Premium UI/UX
Designed with a "Precision Edition" aesthetic, featuring:
- **Glassmorphism**: Advanced CSS-driven blur and semi-transparent layers.
- **Precision Typography**: Optimized for readability using *Inter* and *Outfit* fonts.
- **Cyber-Electric Theme**: A high-contrast, professional dark theme (switchable to light mode).

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd ai_researcher
   ```

2. **Setup environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_key_here
   ```

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## 🛠️ Tech Stack
- **Engine**: OpenAI (GPT-4o / GPT-4 Turbo)
- **Frontend**: Streamlit + Custom CSS (Glassmorphism)
- **Environment**: Python-dotenv
- **Process Management**: Git + .gitignore (API key protection)
