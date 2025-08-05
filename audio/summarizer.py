import openai
from audio.utils import extract_json_block


# 🧠 Generates a structured summary from raw meeting transcript text using OpenAI GPT
def generate_summary(transcript_text):
    
    # 📝 Prompt instructing GPT to act as a business analyst and return JSON
    system_prompt = """
You are an expert business analyst. You will be given a raw transcript from a client-agency meeting.

Your task is to extract a comprehensive and structured summary in JSON format using the schema below.

Please follow these guidelines strictly:
- Be concise but informative. Ensure each bullet is standalone and easy to understand.
- Use consistent formatting (no sentence fragments; start with verbs where applicable).
- For To-Do items, include responsible parties and estimated deadlines if mentioned or inferable.
- Include actionable insights and KPIs if discussed.
- Maintain professional tone. Avoid repetition.

Return **only valid JSON** with no extra text, markdown, or explanation.

Schema:
{
  "mom": ["<Key discussion points and agreements>", "..."],
  "todo_list": ["<Actionable task with responsible person and timeframe, if known>", "..."],
  "action_plan": {
    "decision_made": ["<Key decisions taken>", "..."],
    "key_services_to_promote": ["<Service list>", "..."],
    "target_geography": ["<Location list>", "..."],
    "budget_and_timeline": ["<Budget, timeline details>", "..."],
    "lead_management_strategy": ["<Lead handling strategy>", "..."],
    "next_steps_and_ownership": ["<Task and responsible person>", "..."]
  }
}
"""
    # 🧾 Make a GPT API call using the transcript as input
    chat_response = openai.ChatCompletion.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "system", "content": system_prompt},   # Provides instructions to GPT
            {"role": "user", "content": transcript_text},   # Supplies the raw transcript
        ],
        temperature=0.3,  # Low temperature for deterministic, consistent output
    )

    # 🔍 Extract the JSON content from the GPT response
    return extract_json_block(chat_response.choices[0].message.content)