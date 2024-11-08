
from chat.callbacks import StreamingHandler, END_OF_STREAM
from queue import Queue
from threading import Thread
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            #este coso es blocking, por eso lanzamos otro thread
            self.__call__(input, callbacks=[handler])

        th = Thread(target=task)
        th.start()

        while True:
            token = queue.get()

            if token == END_OF_STREAM:
                break

            yield token
    
class StreamingConversationalRetrievalChain(StreamableChain, ConversationalRetrievalChain):
    pass