document.addEventListener('DOMContentLoaded', function() {
  // Elementos DOM
  const DOM = {
    form: document.getElementById('chat-form'),
    input: document.getElementById('message-input'),
    chat: document.getElementById('chat'),
    welcomeSection: document.getElementById('welcome-section'),
    welcomeMessage: document.getElementById('welcome-message'),
    mainContainer: document.querySelector('.flex-1.flex.flex-col')
  };

  // Configurações
  const CONFIG = {
    userMessage: {
      maxWidth: '65%',
      bgColor: 'bg-slate-500/35',
      padding: 'px-4 py-2',
      borderRadius: 'rounded-xl rounded-br-none',
      textAlign: 'text-left'
    },
    botMessage: {
      maxWidth: '80%',
      padding: 'p-3',
      textPadding: 'px-4 py-2',
      textAlign: 'text-left'
    },
    typewriterSpeed: 20,
    responseDelay: 1000
  };

  /**
   * Efeito de digitação com Tailwind
   * @param {HTMLElement} element - Elemento onde o texto será exibido
   * @param {string} text - Texto a ser digitado
   */
  function typeWriter(element, text) {
    let i = 0;
    element.innerHTML = '<span class="inline-block w-2 h-6 bg-current align-middle animate-blink"></span>';
    function type() {
        if (i < text.length) {
            const cursor = element.querySelector('span');
            if (cursor) {
                element.insertBefore(document.createTextNode(text[i]), cursor);
            }
            i++;
            setTimeout(type, CONFIG.typewriterSpeed);
        } else {
            const cursor = element.querySelector('span');
            if (cursor) cursor.remove();
        }
    }
    type();
}

  /**
   * Cria uma mensagem do usuário
   * @param {string} message - Texto da mensagem
   * @returns {HTMLElement} Elemento da mensagem
   */
  function createUserMessage(message) {
    const container = document.createElement('div');
    container.className = 'flex justify-end';

    const messageElement = document.createElement('div');
    messageElement.className = `${CONFIG.userMessage.maxWidth} ${CONFIG.userMessage.bgColor} ${CONFIG.userMessage.padding} ${CONFIG.userMessage.borderRadius} ${CONFIG.userMessage.textAlign}`;
    messageElement.textContent = message;

    container.appendChild(messageElement);
    return container;
  }

  /**
   * Cria uma resposta do bot
   * @param {string} message - Texto da mensagem
   * @returns {HTMLElement} Elemento da resposta
   */
  function createBotResponse(message) {
    const container = document.createElement('div');
    container.className = 'flex justify-center';

    const wrapper = document.createElement('div');
    wrapper.className = `${CONFIG.botMessage.maxWidth} ${CONFIG.botMessage.padding} text-center`;

    const messageElement = document.createElement('span');
    messageElement.className = `inline-block ${CONFIG.botMessage.textPadding} ${CONFIG.botMessage.textAlign}`;
    messageElement.textContent = message;

    wrapper.appendChild(messageElement);
    container.appendChild(wrapper);
    return container;
  }

  /**
   * Adiciona uma mensagem ao chat e rola para a última mensagem
   * @param {HTMLElement} messageElement - Elemento da mensagem
   */
  function appendMessage(messageElement) {
    DOM.chat.appendChild(messageElement);
    DOM.chat.scrollTop = DOM.chat.scrollHeight;
  }

  /**
   * Processa o envio de mensagem pelo usuário
   * @param {Event} e - Evento de submit
   */
  function handleSubmit(e) {
    e.preventDefault();
    const message = DOM.input.value.trim();
    if (!message) return;
    if (DOM.welcomeSection?.parentNode) {
      DOM.welcomeSection.remove();
      DOM.mainContainer.classList.replace('justify-center', 'justify-end');
    }
    appendMessage(createUserMessage(message));
    DOM.input.value = '';

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: message })
    })
      .then(response => response.json())
      .then(data => {
        const botReply = data.resposta || "Erro: resposta vazia";
        appendMessage(createBotResponse(botReply));
      })
      .catch(error => {
        console.error("Erro ao enviar mensagem:", error);
        appendMessage(createBotResponse("⚠️ Ocorreu um erro ao falar com o FURIABOT."));
      });
  }

  function loadWelcomeMessage() {
    if (!DOM.welcomeMessage) return;
    fetch("/init_message")
      .then((res) => res.json())
      .then((data) => {
        typeWriter(DOM.welcomeMessage, data.mensagem);
      })
      .catch((err) => {
        console.error("Erro:", err);
        document.getElementById('welcome-message').textContent = "⚠️ Erro ao carregar";
      });
  }
  
  // Inicialização
  function init() {
    DOM.form.addEventListener('submit', handleSubmit);
    loadWelcomeMessage();
  }

  init();
});