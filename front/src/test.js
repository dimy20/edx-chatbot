//Esto deberia cambiarse y usar conversaciones creadas por los usuarios, esta demo usa un endpoint con una conversacion y usuarios ya creados.
const url = "http://localhost:9999/api/v1/conversations/85bd17f6-32f5-4066-b86e-35e79a3b6872/messages";

export const api_test = (userText, updateChat) => {
    const data = {
        content: userText,
        user_id: "09de2fc8-f7a2-4363-8981-bcde71942702",
        streaming: true
    };

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.body) {
            throw new Error("ReadableStream not supported in this environment");
        }
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        function readStream() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    console.log("Stream complete");
                    return;
                }
                const chunk = decoder.decode(value, { stream: true });
                updateChat(chunk);  // Call the function to update chat with each chunk
                readStream();  // Continue reading the next chunk
            });
        }

        readStream();
    })
    .catch(error => console.error("Error:", error));
};
