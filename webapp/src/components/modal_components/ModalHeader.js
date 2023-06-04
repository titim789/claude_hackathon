// To-do put the "Investment Apprentice", ticket name, company name, claude rating and assessment and remarks

import { Card } from "@mui/material"
import "./css/ModalHeader.css"

const ModalHeader = ({data}) => {

    return (
        <div className="modalheader">
            <h1>Investment Apprentice</h1>
            <div className="modaltitle">
                <h2>{data.ticker}: {data.company}</h2>
                <div className="rating">
                    <p><b>Rating:</b> {data.rating}/100</p>
                    {data.rate2?<p><b>Claude assessment:</b> {data.rate2}</p>:<></>}
                </div>
            </div>
            <div className="modalsubtitle">
                {data.overall}
            </div>
        </div>
    )

}

export default ModalHeader