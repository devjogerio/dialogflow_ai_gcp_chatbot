import Head from 'next/head';
import ChatInterface from '../components/ChatInterface';

/**
 * Página Principal (Home)
 * Renderiza o layout da aplicação e inclui o componente de chat.
 */
export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <Head>
        <title>Nexus AI - Suporte Inteligente</title>
        <meta name="description" content="Autoatendimento com IA Generativa no GCP" />
      </Head>

      <main className="w-full max-w-4xl flex flex-col items-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Nexus AI
        </h1>
        <p className="text-gray-600 mb-8 text-center">
          Suporte técnico instantâneo powered by Google Vertex AI & Dialogflow
        </p>

        {/* Renderiza o componente de chat isolado */}
        <ChatInterface />

        <footer className="mt-12 text-sm text-gray-500">
          &copy; {new Date().getFullYear()} Nexus Tecnologia - Rodando no Google Cloud Run
        </footer>
      </main>
    </div>
  );
}
