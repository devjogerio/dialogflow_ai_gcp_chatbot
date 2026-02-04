import React, { useState, useRef, useEffect } from 'react';

// Interface para tipagem das mensagens do chat
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

/**
 * Componente ChatInterface
 * Responsável por renderizar a janela de chat, capturar input do usuário
 * e exibir as respostas do bot (Nexus AI).
 */
export default function ChatInterface() {
  // Estado para armazenar o histórico de mensagens
  const [messages, setMessages] = useState<Message[]>([]);
  // Estado para controlar o input de texto
  const [inputText, setInputText] = useState('');
  // Estado para indicar carregamento (typing indicator)
  const [isLoading, setIsLoading] = useState(false);
  // Referência para auto-scroll para o final do chat
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Efeito para rolar a tela sempre que uma nova mensagem chegar
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Função para enviar mensagem para o Backend (Dialogflow)
  const sendMessage = async () => {
    if (!inputText.trim()) return;

    // Adiciona mensagem do usuário ao estado imediatamente (UI otimista)
    const userMsg: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setIsLoading(true);

    try {
      // Simulação de chamada à API do Dialogflow (via Proxy Next.js ou direta)
      // Na produção, isso bateria em um endpoint /api/chat que proxyaria para o Dialogflow CX/ES
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text }),
      });

      const data = await response.json();

      // Adiciona resposta do bot ao estado
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: data.reply || "Desculpe, não entendi.", // Fallback se não houver resposta
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      // Tratamento de erro visual para o usuário
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: "Erro de conexão. Tente novamente mais tarde.",
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
      {/* Cabeçalho do Chat */}
      <div className="bg-blue-600 p-4 text-white font-semibold flex items-center">
        <div className="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
        Nexus AI Suporte
      </div>

      {/* Área de Mensagens */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-10">
            <p>Olá! Sou o Nexus AI.</p>
            <p className="text-sm">Como posso ajudar com seus servidores hoje?</p>
          </div>
        )}
        
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg text-sm ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        
        {/* Indicador de Digitação */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 p-2 rounded-lg text-xs text-gray-500 animate-pulse">
              Nexus AI está digitando...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Área de Input */}
      <div className="p-4 bg-white border-t border-gray-100 flex gap-2">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Digite sua dúvida..."
          className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500 text-sm"
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !inputText.trim()}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
