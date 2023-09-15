import { create } from 'zustand';

interface useDataOutputStore {
    dataOutput: string;
    setDataOutput: (updater: (prevDataOutput: string) => string) => void;
}

export const useDataOutput = create<useDataOutputStore>((set) => ({
    dataOutput: '',
    setDataOutput: (updater: (prevDataOutput: string) => string) => set(state => ({ dataOutput: updater(state.dataOutput) })),
}))