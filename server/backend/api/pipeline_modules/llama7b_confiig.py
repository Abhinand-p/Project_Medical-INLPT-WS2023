import os
from torch import bfloat16
import transformers
from transformers import LlamaTokenizer
from langchain.llms import HuggingFacePipeline 
from dotenv import load_dotenv

class llamaManager:

    def __init__(self):
        load_dotenv()
        model_id = 'meta-llama/Llama-2-7b-chat-hf' 
        hf_auth = os.getenv("HF_API_KEY")
        bnb_config = transformers.BitsAndBytesConfig( load_in_4bit=True, 
                                                    bnb_4bit_quant_type='nf4',
                                                    bnb_4bit_use_double_quant=True, 
                                                    bnb_4bit_compute_dtype=bfloat16 )
        model_config = transformers.AutoConfig.from_pretrained( model_id, token=hf_auth )
        model = transformers.AutoModelForCausalLM.from_pretrained(model_id, 
                                                                trust_remote_code=True,
                                                                config=model_config,
                                                                quantization_config=bnb_config,
                                                                device_map="auto",
                                                                token=hf_auth ) 
        tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf",token=hf_auth)
        generate_text = transformers.pipeline( model=model, tokenizer=tokenizer,
                                            return_full_text=True, 
                                            task='text-generation', 
                                            max_new_tokens=512,
                                            repetition_penalty=1.1, 
                                            use_cache=True,
                                            )
        self.llm = HuggingFacePipeline(pipeline=generate_text)
        

    def query(self, question, context):
        print("###########  LLM: LLAMA 7b")
        prompt = f"""Answer the question with the given Context:
        Query: {question}
        Contexts:
        {context}"""
        answer = self.llm(prompt)
        print(answer)
        return answer
