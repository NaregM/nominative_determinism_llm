NOMINATIVE_DETERMINISM_PROMPT = """
You are an expert in **nominative determinism**—the idea that people’s names
sometimes match their occupations.
**Consider name etymologies and meanings in any language** (English, German, Spanish, Latin, Armenian, Greek, Koreqan, etc.), since a
surname might derive from a word meaning “fire,” “burn,” “ash,” “flame,” or similar in another tongue.

Name: `{name}`
Job Title: `{job_title}`

Respond **only** as valid JSON conforming to the instructions in
`{format_instructions}`.
"""
