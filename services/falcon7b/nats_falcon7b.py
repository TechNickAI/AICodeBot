import asyncio
import nats
import json
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import transformers
device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = "vilsonrodrigues/falcon-7b-instruct-sharded"
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

model_4bit = AutoModelForCausalLM.from_pretrained(
    MODEL, device_map="auto", quantization_config=quantization_config, trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
pipeline = transformers.pipeline(
    "text-generation",
    model=model_4bit,
    tokenizer=tokenizer,
    use_cache=True,
    device_map="auto",
    max_length=2048,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
)
subject_main = "service"
subject = "service.falcon7b"


async def processLLM(msg):
    # decode msg.data into Float32Array from Uint8 of nats. 
    data = json.loads(msg.data.decode())
    response = pipeline(data)
    print("response", response)
    await msg.respond(response.encode())
async def sub():
    # Connect to NATS server
    nc = await nats.connect(servers=["nats://nats_local:4222"], user="falcon7b", password="password")
    print("got nc")
    sub = await nc.subscribe(subject, subject, cb=processLLM)
    print("got sub", sub)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(sub())
loop.run_forever()