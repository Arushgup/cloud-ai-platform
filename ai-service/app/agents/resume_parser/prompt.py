from langchain_core.prompts import ChatPromptTemplate

RESUME_PARSER_PROMPT_V1 = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert resume parser with deep knowledge of technical hiring.

Extract structured information from the resume and return it as a JSON object.

Rules:
1. Extract ONLY information explicitly present. Never infer or fabricate.
2. For dates use format "MMM YYYY" e.g. "Jan 2022".
3. For duration_months calculate from start to end date.
4. For total_experience_years sum all non-overlapping work periods.
5. Separate skills into: programming_languages (Python, Java etc), frameworks_and_tools (FastAPI, Docker etc), skills (everything else).
6. Return null for missing optional fields, empty list for missing arrays.
7. Return ONLY a valid JSON object. No markdown. No explanation. No code blocks.""",
    ),
    (
        "human",
        """Parse this resume into JSON:

---
{resume_text}
---

Return only the JSON object.""",
    ),
])