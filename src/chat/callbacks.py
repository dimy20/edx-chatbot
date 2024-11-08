from langchain.callbacks.base import BaseCallbackHandler
END_OF_STREAM=-1

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
        self.streaming_run_ids = set() #ids of the models whic have streaming enabled

    def on_chat_model_start(self, serialized, messages, run_id, **kwargs):
        if "streaming" in serialized["kwargs"] and serialized["kwargs"]["streaming"]:
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(self, token, *, chunk = None, run_id, parent_run_id = None, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, *, run_id, parent_run_id = None, **kwargs):
        if run_id in self.streaming_run_ids:
            self.queue.put(END_OF_STREAM)
            self.streaming_run_ids.remove(run_id)


    def on_llm_error(self, error, *, run_id, parent_run_id = None, **kwargs):
        self.queue.put(END_OF_STREAM)