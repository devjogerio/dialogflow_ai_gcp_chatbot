import React from 'react';
import { Ticket } from '../types/ticket';

interface TicketTableProps {
    tickets: Ticket[];
}

export default function TicketTable({ tickets }: TicketTableProps) {
    const getStatusColor = (status: string) => {
        switch (status) {
            case 'OPEN': return 'bg-green-100 text-green-800';
            case 'IN_PROGRESS': return 'bg-blue-100 text-blue-800';
            case 'RESOLVED': return 'bg-gray-100 text-gray-800';
            case 'CLOSED': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'CRITICAL': return 'text-red-600 font-bold';
            case 'HIGH': return 'text-orange-600 font-semibold';
            case 'MEDIUM': return 'text-yellow-600';
            case 'LOW': return 'text-blue-600';
            default: return 'text-gray-600';
        }
    };

    return (
        <div className="overflow-x-auto shadow-md sm:rounded-lg">
            <table className="w-full text-sm text-left text-gray-500">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                    <tr>
                        <th scope="col" className="px-6 py-3">ID</th>
                        <th scope="col" className="px-6 py-3">Cliente</th>
                        <th scope="col" className="px-6 py-3">Descrição</th>
                        <th scope="col" className="px-6 py-3">Status</th>
                        <th scope="col" className="px-6 py-3">Prioridade</th>
                        <th scope="col" className="px-6 py-3">Data</th>
                    </tr>
                </thead>
                <tbody>
                    {tickets.map((ticket) => (
                        <tr key={ticket.id} className="bg-white border-b hover:bg-gray-50">
                            <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                #{ticket.id}
                            </td>
                            <td className="px-6 py-4">
                                {ticket.customer_name}
                            </td>
                            <td className="px-6 py-4 truncate max-w-xs" title={ticket.description}>
                                {ticket.description}
                            </td>
                            <td className="px-6 py-4">
                                <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(ticket.status)}`}>
                                    {ticket.status}
                                </span>
                            </td>
                            <td className="px-6 py-4">
                                <span className={`${getPriorityColor(ticket.priority)}`}>
                                    {ticket.priority}
                                </span>
                            </td>
                            <td className="px-6 py-4">
                                {new Date(ticket.created_at).toLocaleDateString('pt-BR')}
                            </td>
                        </tr>
                    ))}
                    {tickets.length === 0 && (
                        <tr>
                            <td colSpan={6} className="px-6 py-4 text-center">
                                Nenhum ticket encontrado.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}
