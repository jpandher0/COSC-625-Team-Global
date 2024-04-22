import {useMancalaGame} from "../contexts/MancalaGameContext";
import {startGame, move, status} from "../services/api.ts";
import {useEffect, useState} from "react";
import {isGameState} from "../types";
import {Link} from "react-router-dom";

type Props = {
    player: number;
    index: number;
};

export const Pit = (props: Props) => {
    const {gameState, setGameState} = useMancalaGame();

    const {index} = props;
    const {player} = props;

    const hasTurn = gameState?.players[player].hasTurn
    const nrOfStones = gameState?.players[player].pits[index]

    const valid = hasTurn && (nrOfStones > 0)

    const onSubmit = async () => {
        const result = await move(index);

        if (isGameState(result)) {
            setGameState(result);
            robot()
        } else {
            console.log(`${result.statusCode} ${result.statusText}`)
        }
    }
    const robot = async () => {
        if (gameState?.gameStatus?.endOfGame) {
            return
        }
        const timer = setTimeout(async () => {
            const result = await status();
            if (isGameState(result)) {
                setGameState(result);
                if (result?.players[1].hasTurn) {
                    robot()
                }
            } else {
                alert(`${result.statusCode} ${result.statusText}`);
            }
        }, 1000)
    }

    return (
        <button onClick={() => onSubmit()} disabled={!valid} style={{width: "120px", height: "120px", border: "none", borderRadius: "10px", fontSize: "26px"}}>
            {gameState?.players[player].pits[index]}
        </button>
    )
}

export const Kalaha = (props: Props) => {
    const {gameState, setGameState} = useMancalaGame();

    const {player} = props;

    return (
        <div style={{display: "flex", alignItems: "center"}}>
            <div style={{width: "150px", height: "300px", borderRadius: "5px", background: "skyblue", padding: "15px"}}>
                {gameState?.players[player].pits[6]}
            </div>
        </div>
    )
}

export const Board = () => {
    const nOfPits = 6;
    const pitsP1 = [];
    const pitsP2 = [];
    const {gameState, setGameState} = useMancalaGame();

    for (let i = 0; i < nOfPits; i++) {
        pitsP1.push(
            <Pit player={0} index={i} key={i}/>
        )
        pitsP2.push(
            <Pit player={1} index={5 - i} key={i}/>
        )
    }
    const human = gameState?.players[0].name
    const robbot = gameState?.players[1].name
    const activePlayer = gameState?.players[0].hasTurn ? human : robbot
    const gameEnded = gameState?.gameStatus.endOfGame
    return (
        <div style={{display: "flex", width: "100%", height: "40vh"}}>
            <div style={{display: "flex", margin: "auto", flexDirection: "row", gap: '25px 25px'}}>
                <Kalaha player={1}/>
                <div style={{display: "flex", flexDirection: "column", gap: '25px 25px'}}>
                    <div style={{display: "flex", gap: "10px 10px"}}>
                        {pitsP2}
                    </div>
                    <div style={{margin: "auto", color: "red"}}>{gameEnded ? "" : `Turn to: ${activePlayer}`}</div>
                    <div style={{display: "flex", gap: "10px 10px"}}>
                        {pitsP1}
                    </div>
                </div>
                <Kalaha player={0}/>
            </div>
        </div>
    )
}

export const Play = () => {
    const {gameState, setGameState} = useMancalaGame();
    const human = gameState?.players[0]
    const robbot = gameState?.players[1]
    const gameEnded = gameState?.gameStatus.endOfGame
    const winner = gameState?.gameStatus.winner
    const onSubmit = async () => {
        const result = await startGame(human.name, robbot.name);

        if (isGameState(result)) {
            setGameState(result);
        } else {
            alert(`${result.statusCode} ${result.statusText}`);
        }
    }

    return (
        <div style={{margin: "auto", fontSize: "32px"}}>
            {gameEnded ?
                <div style={{display: 'flex', flexDirection: "column", margin: 'auto'}}>
                    <div style={{margin: "auto"}}>
                        <div style={{margin: "auto auto 40px auto", fontSize: "60px"}}>Mancala</div>
                        <div style={{margin: "0 auto 40px auto", fontSize: "32px"}}>{winner}</div>
                        <div>Your Score：{human?.pits[human?.pits.length - 1]}</div>
                        <div>Computer Score：{robbot?.pits[robbot?.pits.length - 1]}</div>
                    </div>
                    <button onClick={() => onSubmit()} style={{margin: "auto", marginTop: '30px', width: '200px', height: '50px', border: "none", fontSize: "26px"}}>Play Agian</button>
                </div>
                :
                <>
                    <div style={{display: 'flex', justifyContent: 'space-between', margin: 'auto'}}>
                        <Link to="/">
                            <button style={{width: '200px', height: '60px', border: 'none', fontSize: "26px"}}>Exit</button>
                        </Link>
                        <div style={{}}>
                            <div>Score</div>
                            <div>You：{human?.pits[human?.pits.length - 1]}</div>
                            <div>Computer：{robbot?.pits[robbot?.pits.length - 1]}</div>
                        </div>
                    </div>
                    <div style={{display: "flex", flexDirection: "column", width: "100%"}}>
                        <h4 style={{margin: "0 auto"}}>{robbot?.name}</h4>
                        <Board/>
                        <h4 style={{margin: "0 auto"}}>{human?.name}</h4>
                    </div>
                </>
            }
        </div>
    )
};

export const Start = () => {
    const {setGameState} = useMancalaGame();

    const [human, setHuman] = useState("");
    const [robot, setRobot] = useState("COSC 625 Aibot");
    const valid = human !== "" && robot !== "" && human !== robot;

    const onSubmit = async () => {
        const result = await startGame(human, robot);

        if (isGameState(result)) {
            setGameState(result);
        } else {
            alert(`${result.statusCode} ${result.statusText}`);
        }
    }

    return (
        <div style={{display: "flex", margin: "auto"}}>
            <form style={{margin: 'auto', display: "flex", flexDirection: "column", gap: '10px 10px'}}>
                <input placeholder={'Player name'} style={{width: "300px", height: "40px", padding: '0 10px', border: 'none', borderRadius: '5px'}} value={human} onChange={e => setHuman(e.target.value)}/>
                {/*<input placeholder={'AI name'} style={{width: "300px", height: "40px", padding: '0 10px'}} value={robot} onChange={e => setRobot(e.target.value)}/>*/}
                {
                    valid ? <button
                        style={{border: "none", background: 'lightgray', padding: '10px', border: 'none', borderRadius: '10px'}}
                        type="button"
                        onClick={() => onSubmit()}>
                        Start
                    </button> : ''
                }
            </form>
        </div>
    );
};

export const Mancala = () => {
    const {gameState} = useMancalaGame();
    return gameState ? <Play/> : <Start/>;
};
