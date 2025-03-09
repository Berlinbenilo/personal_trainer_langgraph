from typing import Dict

from langchain_openai import ChatOpenAI
from langchain.chat_models import ChatOllama
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.utils.prompt_utils import PromptJinjaTemplate


def llm_factory(model_config, model_provider) -> BaseChatModel:
    model = None
    if model_provider == "openai":
        model = ChatOpenAI(**model_config[model_provider])
    elif model_provider == "ollama":
        model = ChatOllama(**model_config[model_provider])

    if model is None:
        raise KeyError(f"Model type {model_provider} not found")
    return model


class LLMWrapper(object):
    def __init__(self, model_config: dict, model_provider: str):
        self.llm = llm_factory(model_config, model_provider)
        self.cached_chains = {}

    @staticmethod
    def set_prompt(prompt, input_values):
        template = PromptJinjaTemplate(template=prompt, input_variables=list(input_values.keys()))

        return template.format(**input_values)

    async def invoke_with_parser(self, prompt: str, placeholder_input: Dict = None,
                                 output_validator=None,
                                 stream: bool = False):
        prompt_template = self.set_prompt(prompt=prompt, input_values=placeholder_input)
        _parser = JsonOutputParser(pydantic_object=output_validator) if output_validator else StrOutputParser()

        prompt = PromptTemplate.from_template(
            template=prompt_template,
            partial_variables={"format_instructions": _parser.get_format_instructions() if output_validator else ""},
        )
        chain = prompt | self.llm | _parser

        if stream:
            return self._invoke_streaming(chain, {})
        parsed_response = await chain.ainvoke({})
        return parsed_response

    @staticmethod
    async def _invoke_streaming(chain, input_data: Dict):
        response_generator = chain.astream(input_data)
        async for partial_response in response_generator:
            yield partial_response
