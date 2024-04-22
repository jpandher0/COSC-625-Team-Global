import {Link} from "react-router-dom";

export const About = () => {
    return (
        <div style={{display: "flex", flexDirection: "column", width: "100%", margin: "auto 400px"}}>
            <Link to="/">
                <button style={{width: '200px', height: '60px', border: 'none', borderRadius: '5px', fontSize: "32px"}}>Back</button>
            </Link>
            <h1 style={{display: "flex", margin: "10px auto"}}>Mancala Instrution</h1>
            <p>
                Mancala is a traditional board game known for its simple yet strategic gameplay. Each player has a row of six small pits and a larger pit (store) to their right. The game starts with four pieces in each of the smaller pits.
                Players take turns picking all pieces from one of their pits, then distributing them one-by-one into subsequent pits (including their own store but not their opponent's) in a counterclockwise direction. If the last piece lands in an empty pit on their side, they capture all pieces in the opposite pit, placing them in their store.
                The game ends when one player's side is empty, with the remaining pieces on the other side going to that player's store. The player with the most pieces in their store at the end is the winner.
                Key rules include earning an extra turn if the last piece lands in your store, and the strategy of choosing which pit to start from to maximize piece capture or continue playing.
            </p>
        </div>
    )
}
