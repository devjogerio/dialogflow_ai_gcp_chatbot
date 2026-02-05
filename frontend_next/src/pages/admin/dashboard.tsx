import React, { useEffect, useState } from 'react';
import TicketTable from '../../components/TicketTable';
import { ticketService } from '../../services/ticketService';
import { Ticket } from '../../types/ticket';

export default function Dashboard() {
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        loadTickets();
    }, []);

    const loadTickets = async () => {
        try {
            const data = await ticketService.getTickets();
            setTickets(data);
        } catch (err) {
            setError('Erro ao carregar tickets. Verifique se o backend está rodando.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Dashboard de Atendimentos</h1>
                    <button 
                        onClick={loadTickets}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        Atualizar
                    </button>
                </div>

                {loading ? (
                    <div className="text-center py-10">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-600">Carregando tickets...</p>
                    </div>
                ) : error ? (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                        <strong className="font-bold">Erro!</strong>
                        <span className="block sm:inline"> {error}</span>
                    </div>
                ) : (
                    <TicketTable tickets={tickets} />
                )}
            </div>
        </div>
    );
}
