export type GameState = {
    players: [Player, Player];
    gameStatus: {
        endOfGame: boolean;
        winner: string;
    };
}

export type Player = {
    name: string;
    pits: Pit[];
    hasTurn: boolean;
}

export type Pit = {
    index: number;
    nrOfStones: number;
}

export function isGameState(gameState: unknown): gameState is GameState {
    return (gameState as GameState).players !== undefined;
}
