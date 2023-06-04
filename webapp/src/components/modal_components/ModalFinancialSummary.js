// To-do add the financial summary
import "./css/ModalFinancialSummary.css"

const ModalFinancialSummary = ({data}) => {

    

    return(
        <div className="financialsummary">
            <h3>Financial Summary</h3>
            <table>
                {Object.keys(data.financials).map((key) => {
                    console.log(key)
                    return (<tr><th>{key}:</th><td>{data.financials[key]}</td></tr>)
                })}
            </table>
        </div>
    )
}

export default ModalFinancialSummary