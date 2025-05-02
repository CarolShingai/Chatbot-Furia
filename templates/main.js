document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM
    const DOM = {
      form: document.getElementById('chat-form'),
      input: document.getElementById('message-input'),
      chat: document.getElementById('chat'),
      welcomeSection: document.querySelector('.flex.flex-col.items-center.gap-2.text-center.opacity-90'),
      mainContainer: document.querySelector('.flex-1.flex.flex-col')
    };
  
    // Configurações
    const CONFIG = {
      userMessage: {
        maxWidth: '65%',
        bgColor: 'bg-slate-500/35',
        padding: 'px-4 py-2',
        borderRadius: 'rounded-xl rounded-br-none'
      },
      botMessage: {
        maxWidth: '80%',
        padding: 'p-3',
        textPadding: 'px-4 py-2'
      },
      responseDelay: 1000
    };
  
    /**
     * Cria uma mensagem do usuário
     * @param {string} message - Texto da mensagem
     * @returns {HTMLElement} Elemento da mensagem
     */
    function createUserMessage(message) {
      const container = document.createElement('div');
      container.className = 'flex justify-end mr-60';
      
      const messageElement = document.createElement('div');
      messageElement.className = `${CONFIG.userMessage.maxWidth} ${CONFIG.userMessage.bgColor} ${CONFIG.userMessage.padding} ${CONFIG.userMessage.borderRadius}`;
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
      messageElement.className = `inline-block ${CONFIG.botMessage.textPadding}`;
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
      
      // Remove a seção de boas-vindas na primeira mensagem
      if (DOM.welcomeSection) {
        DOM.welcomeSection.remove();
        DOM.welcomeSection = null;
        DOM.mainContainer.classList.remove('justify-center');
        DOM.mainContainer.classList.add('justify-end');
      }
      
      // Adiciona mensagem do usuário
      appendMessage(createUserMessage(message));
      DOM.input.value = '';
      
      // Simula resposta do bot
      setTimeout(() => {
        appendMessage(createBotResponse(`Resposta simulada para: "${message}"`));
      }, CONFIG.responseDelay);
    }
  
    // Inicialização
    function init() {
      DOM.form.addEventListener('submit', handleSubmit);
    }
  
    init();
});