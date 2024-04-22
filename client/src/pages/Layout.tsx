import {Link} from "react-router-dom";

export const Layout = () => {

    return (
        <div style={{display: "flex", flexDirection: "column", margin: "auto"}}>
            <div style={{margin: "-150px auto 100px auto", fontSize: "60px"}}>Mancala</div>
            <div style={{display: "flex", gap: '20px', justifyContent: 'center', margin: '20px 0 0 0'}}>
                <Link to="/mancala">
                    <button  style={{width: '200px', height: '70px', border: 'none', borderRadius: '10px', fontSize: "32px"}}>Enter</button>
                </Link>
                <Link to="/about">
                    <button  style={{width: '200px', height: '70px', border: 'none', borderRadius: '10px', fontSize: "32px"}}>Instrution</button>
                </Link>
            </div>
        </div>
    )
};
