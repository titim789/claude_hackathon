//compfin, change, reasons,

import "./css/ModalPrevQuarterCompare.css"

const ModalPrevQuarterCompare = ({data}) => {

    return (
        <div className="prevquartercompare">
            {(data.compfin || data.change || data.reasons) && <h3>Compared to Previous Quarter</h3>}
            <ul>
                {data.compfin && <li>{data.compfin}</li>}
                {data.change && <li>{data.change}</li>}
                {data.reasons && <li>{data.reasons}</li>}
            </ul>
        </div>
    )
}

export default ModalPrevQuarterCompare