import { Ticket } from '../types/ticket';
import { getCookie } from '../utils/auth';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_URL = `${BASE_URL}/api/tickets/`;

export const ticketService = {
  async getTickets(): Promise<Ticket[]> {
    try {
      const response = await fetch(API_URL, {
        credentials: 'include',
      });
      if (!response.ok) {
        if (response.status === 403 || response.status === 401) {
          throw new Error('Não autorizado');
        }
        throw new Error('Falha ao buscar tickets');
      }
      return await response.json();
    } catch (error) {
      console.error('Erro no ticketService:', error);
      throw error;
    }
  },

  async createTicket(
    ticket: Omit<Ticket, 'id' | 'created_at' | 'updated_at'>,
  ): Promise<Ticket> {
    try {
      const csrfToken = getCookie('csrftoken');
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
        body: JSON.stringify(ticket),
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Falha ao criar ticket');
      }
      return await response.json();
    } catch (error) {
      console.error('Erro no ticketService:', error);
      throw error;
    }
  },
};
