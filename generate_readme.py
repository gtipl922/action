mport os
import requests
import json
import subprocess

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
README_FILE = "README.md"

# --- Functions ---

def get_project_description():
    """
    In a real-world scenario, this function would analyze the repository
    to gather information for the AI prompt. This is a simplified version.
    You could read file names, a manifest file (like package.json), or
    look for specific code comments to build a detailed description.
    """
    # Placeholder: In a real script, you'd analyze the repo contents here.
    # For this example, we'll use a hardcoded description.
    return "A Python-based utility that automates the generation of professional README.md files for a GitHub repository using the Gemini API. It is designed to run as a GitHub Action."

def generate_readme_content(project_description):
    """
    Calls the Gemini API to generate the README content.
    """
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    headers = {
        "Content-Type": "application/json"
    }

    system_prompt = """
    You are a professional README file generator. Your task is to create a comprehensive, well-structured, and visually appealing README.md in Markdown format. The README should be based on the provided project description. Include:
    1. A placeholder for a professional logo at the top.
    2. A title and a concise description.
    3. Badges for build status, license, and other relevant metrics (use placeholders).
    4. A comprehensive Features section with clear explanations and emojis or icons for each feature.
    5. A Technologies Used section with a list of key technologies.
    6. Detailed Installation and Usage instructions.
    7. A section on Contributing.
    8. A clear License section.
    Use appropriate headings, lists, and code blocks to make the file look polished and professional.
    """

    user_query = f"Generate a README file for the following project: {project_description}"
    
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

def update_and_commit_readme(content):
    """
    Writes the content to the README file and commits the changes.
    """
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)
        
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    
    subprocess.run(["git", "add", README_FILE])
    
    commit_message = "docs: Auto-generate README using AI"
    result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True)
    
    if "nothing to commit" in result.stdout.decode("utf-8"):
        print("No changes to README.md. Nothing to commit.")
    else:
        subprocess.run(["git", "push"])
        print("Successfully updated and committed README.md.")

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting README generation...")
    
    project_description = get_project_description()
    if not project_description:
        print("Could not get project description. Exiting.")
    else:
        readme_content = generate_readme_content(project_description)
        if readme_content:
            update_and_commit_readme(readme_content)
        else:
            print("Failed to generate README content.")
