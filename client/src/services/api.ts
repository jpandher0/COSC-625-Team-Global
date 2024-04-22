import { GameState } from "../types";

export async function startGame(human: string, robot: string) {
    const response = await fetch("mancala/start", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify([
            human, robot
        ]),
    });

    if (response.ok) {
        const gameState = await response.json();
        return gameState as GameState;
    } else {
        return {
            statusCode: response.status,
            statusText: response.statusText
        };
    }
}

export async function move(index: number) {
    const response = await fetch("mancala/move?index=" + (index + 1), {
        method: "GET",
        headers: {
            Accept: "application/json",
        }
    });

    if (response.ok) {
        const gameState = await response.json();
        return gameState as GameState;
    } else {
        return {
            statusCode: response.status,
            statusText: response.statusText
        };
    }
}

export async function status() {
    const response = await fetch("mancala/status", {
        method: "GET",
        headers: {
            Accept: "application/json",
        }
    });

    if (response.ok) {
        const gameState = await response.json();
        return gameState as GameState;
    } else {
        return {
            statusCode: response.status,
            statusText: response.statusText
        };
    }
}
