import openai
import json
import os
import re
from dotenv import load_dotenv

# 🔐 Load environment variables from .env (including OpenAI key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


# 📊 Summarizes raw website content into a structured JSON using OpenAI GPT
def summarize_with_openai(webpage_text):
    
    # 📜 Construct the detailed prompt with exact format instructions
    prompt = f"""
You are a professional business analyst. Analyze the following website content and extract comprehensive, detailed business information in JSON format.

Each section should contain **4–6 bullet points** with rich, descriptive details — not short or generic phrases. Bold important keywords using `**bold**` markdown format. DO NOT include explanations, just return the valid JSON only.

Use this exact structure:

{{
  "title": "<Website Title or Company Name>",
  "sections": [
    {{
      "heading": "Purpose",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Target Audience",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "About the Company",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Company Information",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Unique Selling Proposition (USP)",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Reviews/Testimonials",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Products/Service Categories",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Offers",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }}
  ]
}}

Analyze this content:
\"\"\"{webpage_text}\"\"\"
"""
    # 🤖 Send request to GPT with structured prompt
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,  # Low temp for consistent, deterministic structure
        )

        # 🧾 Extract response text
        raw_text = response["choices"][0]["message"]["content"].strip()
        raw_text = raw_text.strip("`").strip()

        # 🔍 Remove any "json" label prefix if present
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

       # 🔧 Normalize problematic characters (smart quotes, dashes, etc.)
        raw_text = (
            raw_text.replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("‘", "'")
            .replace("–", "-")
            .replace("—", "-")
        )

        # 🧠 Extract valid JSON block using regex
        match = re.search(r"{.*}", raw_text, re.DOTALL)
        json_text = match.group(0) if match else raw_text

        return json.loads(json_text)

    # ❌ Handle failures in GPT response or JSON parsing
    except Exception as e:
        print("⚠️ OpenAI JSON parsing failed:", e)
        print("⚠️ Raw output was:\n", raw_text)
        
        # Return fallback default structure
        return {
            "title": "Summary Unavailable",
            "sections": [
                {
                    "heading": "Error",
                    "content": "OpenAI returned invalid or incomplete JSON.",
                }
            ],
        }