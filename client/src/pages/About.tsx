import {Link} from "react-router-dom";

export const About = () => {
    return (
        <div style={{padding: '30px'}}>
            <Link to="/">
                <button style={{width: '150px', height: '50px', border: 'none'}}>Back</button>
            </Link>
            <article>
                <h1>Mancala Instruction</h1>
                <p>
                 Equipment:
                     Mancala board: Consists of 12 smaller pits in two rows of six each, and two larger pits (stores) at either end.
                     Stones: 48 stones or seeds used as playing pieces.
                 Setup:
                    Place 4 stones in each of the 12 smaller pits.
                Objective:
                    Collect more stones in your store (the large pit to your right) than your opponent.
                How to Play:
                    Turns: Players take turns, starting with one player.
                    Sowing: On your turn, pick up all the stones in any one of your pits. Dropping one stone in each pit counter-clockwise, including your store but skipping your opponent's store.
                    Capturing: If the last stone you drop lands in an empty pit on your side and there are stones in the opposite pit, you capture all stones in both pits (yours and the opposite one) and place them in your store.
                    Extra Turn: If the last stone you drop lands in your store, you get another turn.
                Ending the Game:
                    The game ends when all pits on one side of the board are empty.
                    The player with remaining stones on their side of the board moves all of them to their store.
                    Count the stones in each store. The player with the most stones wins the game.
                </p>
            </article>
        </div>
    )
}
