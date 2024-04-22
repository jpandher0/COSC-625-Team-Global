import {Link} from "react-router-dom";

export const Layout = () => {

    return (
        <div style={{width: '100%', display: "flex", flexDirection: "column"}}>
            <div style={{margin: "auto"}}>Mancala</div>
            <div style={{width: '100%', display: "flex", gap: '20px', justifyContent: 'center', margin: '20px 0 0 0'}}>
                <Link to="/mancala">
                    <button  style={{width: '150px', height: '50px'}}>Enter</button>
                </Link>
                <Link to="/about">
                    <button  style={{width: '150px', height: '50px'}}>Instruction</button>
                </Link>
            </div>
        </div>
    )
};
