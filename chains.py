from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables.base import Runnable

from prompts import NOMINATIVE_DETERMINISM_PROMPT
from schemas import NDResult

import os
from dotenv import find_dotenv, load_dotenv

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------

_ = load_dotenv()

parser = PydanticOutputParser(pydantic_object=NDResult)

prompt = PromptTemplate(
    template=NOMINATIVE_DETERMINISM_PROMPT,
    input_variables=["name", "job_title"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


def make_nd_chain_gpt(model_name: str = "gpt-4o",
                      temp: float = 0.0) -> Runnable:
    """
    """
    
    llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"),
                     temperature = temp,
                     model = model_name)

    chain_gpt = prompt | llm | parser
    
    return chain_gpt