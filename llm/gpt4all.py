from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def get_gpt4all_llm(local_path='C:\GPT4ALL\gpt4all-lora-quantized-ggml_converted.bin'):
    callbacks = [StreamingStdOutCallbackHandler()]
    # Verbose is required to pass to the callback manager
    llm = GPT4All(model=local_path,  n_ctx=10000, n_threads=8, callbacks=callbacks, verbose=True)
    return llm

