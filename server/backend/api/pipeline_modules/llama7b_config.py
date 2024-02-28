import os
from torch import bfloat16
import transformers
from transformers import LlamaTokenizer
from langchain.llms import HuggingFacePipeline 
from dotenv import load_dotenv
from utils import Utils

class LlamaManager:

    def __init__(self):
        load_dotenv()
        model_id = 'meta-llama/Llama-2-7b-chat-hf' 
        hf_auth = os.getenv("HF_API_KEY")
        self.utils = Utils()
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
        self.history = []

    def query(self, question, context):
        if len(question) == 0 or len(context) == 0:
            pass
        else:
            print("###########  LLM: LLAMA 7b")
            augmented_prompt = f"1- Answer the question with the given Contexts.2- If it is not possible to answer based on given contexts, use the the following template and answer based on your knowledge.\n ``` There is no such data on provided Articles, However, based on my knowledge, I can say that... \n 3- If there are previous conversations use them as well. ``` \nQuestion:\n{question} \nContexts:\n{context}"
            self.history.append(question)
            answer = self.llm(augmented_prompt)
            if not self.utils.extract_context(answer):
                self.history.append(answer)
                self.utils.save_conversation(self.history, Geneartor='LLAMA')
            print(answer)
            return answer
