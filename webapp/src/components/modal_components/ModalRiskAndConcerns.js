//To-do add a card to display the decription of the risks and concerns of the company

import "./css/ModalRiskAndConcerns.css"

const ModalRiskAndConcerns = ({data}) => {

    return (
        <div className="riskandconcerns">
            <h3>Ricks & Concerns</h3>
            <p>{data.qa}</p>
        </div>
    )
}

export default ModalRiskAndConcerns