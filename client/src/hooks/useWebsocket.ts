import { useRef, useCallback, useEffect } from 'react';
import WebSocket from 'isomorphic-ws';
import { getHostName } from '@/utils/urlUtils';

const useWebsocket = () => {
    const socketRef = useRef<WebSocket | null>(null);
  
    const connectSocket = useCallback(() => {
      if (!socketRef.current || socketRef.current.readyState === WebSocket.CLOSED) {
        const { protocol } = window.location;
        socketRef.current = new WebSocket(`${protocol === 'https:' ? 'wss:' : 'ws:'}//${getHostName()}/ws`);
  
        socketRef.current.onopen = () => {
          console.log('WebSocket is connected.');
        };
  
        socketRef.current.onerror = (error: Event) => {
          console.log('WebSocket Error: ', error);
        };
  
        socketRef.current.onclose = (event: CloseEvent) => {
          console.log('WebSocket connection closed: ', event.code);
        };
      }
    }, []);
  
    const send = useCallback((message: string) => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(message);
      }
    }, []);
  
    const close = useCallback(() => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.close();
      }
    }, []);
  
    useEffect(() => {
      connectSocket();
      return () => {
        close();
      };
    }, [connectSocket, close]);
  
    return { send, close, socketRef };
};
  
export default useWebsocket;