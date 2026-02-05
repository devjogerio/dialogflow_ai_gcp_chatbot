import { Ticket } from '../types/ticket';

const API_URL = 'http://localhost:8000/api/tickets/';

export const ticketService = {
    async getTickets(): Promise<Ticket[]> {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error('Falha ao buscar tickets');
            }
            return await response.json();
        } catch (error) {
            console.error('Erro no ticketService:', error);
            throw error;
        }
    },

    async createTicket(ticket: Omit<Ticket, 'id' | 'created_at' | 'updated_at'>): Promise<Ticket> {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(ticket),
            });
            if (!response.ok) {
                throw new Error('Falha ao criar ticket');
            }
            return await response.json();
        } catch (error) {
            console.error('Erro no ticketService:', error);
            throw error;
        }
    }
};
