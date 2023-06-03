import powerByIcon from "../assets/images/powered_by_anthropic_transparent.png"
import "./css/Footer.css"

const Footer = () => {
    return (
        <div className="footer">
            <img src={powerByIcon} style={{ width: "200px", height: "50px" }}/>
        </div>
    )
}

export default Footer