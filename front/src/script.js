import { api_test } from "./test";

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

export function sendMessage() {
  const userInput = document.getElementById('userInput');
  const chatHistory = document.getElementById('chatHistory');

  if (userInput.value.trim() === "") return;

  const userText = userInput.value;

  // Display user's message in the chat
  const userMessage = document.createElement('div');
  userMessage.className = 'flex justify-end mb-2';
  userMessage.innerHTML = `
    <div class="${isAlternate ? 'bg-gray-300' : 'bg-gray-200'} text-gray-800 p-3 rounded-lg shadow-md">
      ${userText}
    </div>
  `;
  chatHistory.appendChild(userMessage);
  chatHistory.scrollTop = chatHistory.scrollHeight;  // Scroll to the bottom
  userInput.value = "";

  // Placeholder for the bot message container
  const botMessage = document.createElement('div');
  botMessage.className = 'flex justify-start items-center space-x-2 mb-2';
  const botTextContainer = document.createElement('div');
  botTextContainer.className = `${isAlternate ? 'bg-gray-300' : 'bg-gray-200'} text-gray-800 p-3 rounded-lg shadow-md`;
  botMessage.appendChild(botTextContainer);
  chatHistory.appendChild(botMessage);
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Function to update chat with each streamed chunk and format it
  function updateChat(chunk) {
    // Format the chunk as HTML
    const formattedChunk = formatResponseText(chunk);
    botTextContainer.innerHTML += formattedChunk;
    chatHistory.scrollTop = chatHistory.scrollHeight;  // Keep scroll at bottom
  }

  // Call api_test with the user text and updateChat function
  api_test(userText, updateChat);

  isAlternate = !isAlternate;  // Toggle message color for next message
}

// Simple function to format text with basic HTML elements
function formatResponseText(text) {
  // Convert line breaks to HTML <br>
  text = text.replace(/\n/g, "<br>");

  // Convert markdown-like lists (e.g., "1. ", "- ") into HTML lists
  text = text.replace(/(\d+\.) (.+)/g, '<li>$2</li>'); // Numbered lists
  text = text.replace(/- (.+)/g, '<li>$1</li>'); // Bullet lists

  // Wrap <li> elements with <ul> tags for lists
  text = text.replace(/(<li>.*<\/li>)/g, "<ul>$1</ul>");

  return text;
}

// Function to start a conversation with the course name
export function startConversation() {
  const courseInput = document.getElementById('courseInput').value.trim();
  const courseTitle = document.getElementById('selectedCourseTitle');
  const courseHeader = document.getElementById('courseHeader');
  const courseList = document.getElementById('courseList');
  const userInput = document.getElementById('userInput');
  const sendMessageButton = document.getElementById('sendMessageButton');

  if (courseInput) {
    // Update the course title with a fade-in effect
    courseHeader.classList.add('opacity-0'); // Fade out header text
    setTimeout(() => {
      courseTitle.textContent = `Conversación para: ${courseInput}`;
      courseTitle.classList.remove('opacity-0'); // Fade in new title
      courseHeader.textContent = courseInput;
      courseHeader.classList.remove('opacity-0');
    }, 500);

    // Enable chat input and send button after starting a conversation
    userInput.disabled = false;
    sendMessageButton.disabled = false;

    // Add the course to the chat history list
    const newCourseItem = document.createElement('li');
    newCourseItem.innerHTML = `<a href="#" onclick="selectCourse(this)" class="block p-2 rounded hover:bg-green-700">${courseInput}</a>`;
    courseList.appendChild(newCourseItem);

    // Clear the course input field
    document.getElementById('courseInput').value = '';
  } else {
    alert("Por favor, ingresa un nombre de curso.");
  }
  const chatHistory = document.getElementById('chatHistory');
  const welcomeMessage = document.createElement('div');
  welcomeMessage.className = 'flex justify-start items-center space-x-2 mb-2';
  welcomeMessage.innerHTML = `
  <div class="bg-gray-200 text-gray-800 p-3 rounded-lg shadow-md">
    ¡Hola! ¿En qué puedo ayudarte hoy?
  </div>
`;
  chatHistory.appendChild(welcomeMessage);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

window.sendMessage = sendMessage;
window.selectCourse = selectCourse;
window.startConversation = startConversation;
