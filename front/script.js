
let currentSelected = null;
let isAlternate = false; 

function selectCourse(element) {
  if (currentSelected) {
    currentSelected.classList.remove('bg-green-600');
  }

  
  element.classList.add('bg-green-600');
  document.getElementById('selectedCourseTitle').textContent = `Historial para: ${element.textContent}`;

  
  currentSelected = element;
}

function sendMessage() {
  const userInput = document.getElementById('userInput');
  const chatHistory = document.getElementById('chatHistory');

  if (userInput.value.trim() === "") return; 

  
  const userMessage = document.createElement('div');
  userMessage.className = 'flex justify-end mb-2';
  userMessage.innerHTML = `
    <div class="${isAlternate ? 'bg-gray-300' : 'bg-gray-200'} text-gray-800 p-3 rounded-lg shadow-md">
      ${userInput.value}
    </div>
  `;
  chatHistory.appendChild(userMessage);

  
  const userText = userInput.value;
  userInput.value = "";

  
  setTimeout(() => {
    const botMessage = document.createElement('div');
    botMessage.className = 'flex justify-start items-center space-x-2 mb-2';
    botMessage.innerHTML = `
      <div class="${isAlternate ? 'bg-gray-300' : 'bg-gray-200'} text-gray-800 p-3 rounded-lg shadow-md">
        Esta es una respuesta automática a tu mensaje: "${userText}"
      </div>
      <div class="flex items-center space-x-2">
        <button onclick="rateMessage(this, '👍')" class="bg-gray-600 hover:bg-gray-700 text-white p-2 rounded-md focus:outline-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 9V5a3 3 0 10-6 0v4H5a2 2 0 00-2 2v8a2 2 0 002 2h14a2 2 0 002-2v-8a2 2 0 00-2-2h-5z" />
          </svg>
        </button>
        <button onclick="rateMessage(this, '👎')" class="bg-gray-600 hover:bg-gray-700 text-white p-2 rounded-md focus:outline-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 15v4a3 3 0 006 0v-4h5a2 2 0 002-2v-8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2h5z" />
          </svg>
        </button>
      </div>
    `;
    chatHistory.appendChild(botMessage);
    chatHistory.scrollTop = chatHistory.scrollHeight; 

    
    isAlternate = !isAlternate;
  }, 500);
}


function rateMessage(button, rating) {
  button.parentNode.innerHTML = `<span class="text-sm text-gray-400">${rating} Gracias por tu retroalimentación</span>`;
}
