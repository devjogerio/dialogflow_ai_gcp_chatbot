import React from 'react';
import { render, screen } from '@testing-library/react';
import TicketTable from '../components/TicketTable';
import { Ticket } from '../types/ticket';

const mockTickets: Ticket[] = [
    {
        id: 1,
        customer_name: 'João Silva',
        description: 'Erro no login',
        status: 'OPEN',
        priority: 'HIGH',
        created_at: '2023-10-01T10:00:00Z',
        updated_at: '2023-10-01T10:00:00Z'
    },
    {
        id: 2,
        customer_name: 'Maria Souza',
        description: 'Dúvida sobre fatura',
        status: 'RESOLVED',
        priority: 'LOW',
        created_at: '2023-10-02T14:30:00Z',
        updated_at: '2023-10-02T15:00:00Z'
    }
];

describe('TicketTable Component', () => {
    it('deve renderizar a tabela corretamente', () => {
        render(<TicketTable tickets={mockTickets} />);
        
        // Verifica cabeçalhos
        expect(screen.getByText('ID')).toBeInTheDocument();
        expect(screen.getByText('Cliente')).toBeInTheDocument();
        expect(screen.getByText('Status')).toBeInTheDocument();

        // Verifica dados do primeiro ticket
        expect(screen.getByText('João Silva')).toBeInTheDocument();
        expect(screen.getByText('Erro no login')).toBeInTheDocument();
        expect(screen.getByText('OPEN')).toBeInTheDocument();
        expect(screen.getByText('HIGH')).toBeInTheDocument();

        // Verifica dados do segundo ticket
        expect(screen.getByText('Maria Souza')).toBeInTheDocument();
        expect(screen.getByText('RESOLVED')).toBeInTheDocument();
    });

    it('deve exibir mensagem quando não houver tickets', () => {
        render(<TicketTable tickets={[]} />);
        expect(screen.getByText('Nenhum ticket encontrado.')).toBeInTheDocument();
    });

    it('deve aplicar classes de cores corretas para status', () => {
        render(<TicketTable tickets={mockTickets} />);
        
        const openBadge = screen.getByText('OPEN');
        expect(openBadge).toHaveClass('bg-green-100');

        const resolvedBadge = screen.getByText('RESOLVED');
        expect(resolvedBadge).toHaveClass('bg-gray-100');
    });
});
