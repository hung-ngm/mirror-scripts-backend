import WebSocket from 'isomorphic-ws';
import { getHostName } from './urlUtils';

let socket: WebSocket | null = null;

export function connectSocket(): WebSocket {
    if (!socket || socket.readyState === WebSocket.CLOSED) {
        const { protocol } = window.location;
        socket = new WebSocket(`${protocol === 'https:' ? 'wss:' : 'ws:'}://${getHostName()}/ws`);

        socket.onopen = () => {
          console.log('WebSocket is connected.');
        };
    
        socket.onerror = (error: ErrorEvent) => {
          console.log('WebSocket Error: ', error);
        };
    
        socket.onclose = (event: CloseEvent) => {
          console.log('WebSocket connection closed: ', event.code);
        };
    }
    
    return socket;
}

export function sendSocketMessage(message: string): void {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    }
}

export function closeSocket(): void {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
    }
}