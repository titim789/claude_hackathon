// To-do add the financial summary
import "./css/ModalFinancialSummary.css"

const ModalFinancialSummary = ({data}) => {


    return(
        <div className="financialsummary">
            <h3>Financial Summary</h3>
            <table>
                <tr><th>Net Sales: </th><td>{data.financial_summary.net_sales}</td></tr>
                <tr><th>Earnings per share: </th><td>{data.financial_summary.earnings_per_share}</td></tr>
                <tr><th>Operating Income: </th><td>{data.financial_summary.operating_income}</td></tr>
                <tr><th>Gross Margin: </th><td>{data.financial_summary.gross_margin}</td></tr>
            </table>
        </div>
    )
}

export default ModalFinancialSummary