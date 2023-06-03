import {Box, Modal} from "@mui/material"
import ModalHeader from "./modal_components/ModalHeader";
import ModalFinancialSummary from "./modal_components/ModalFinancialSummary";
import ModalKeyPoints from "./modal_components/ModalKeyPoints";
import ModalRiskAndConcerns from "./modal_components/ModalRiskAndConcerns";
import ModalCloseButton from "./modal_components/ModalCloseButton";
import ModalCompareButton from "./modal_components/ModalCompareButtons";


const CustomModal = ({data, modalOpen, setModalOpen}) => {

    const mock_data = {
        company: data.company,
        rating: data.rating,
        remarks: data.remarks,
        ticket: data.company, // to be changed to the actual ticket of the company
        assessment: "Deteriorating",
        financial_summary: {
            net_sales: "620 billion",
            earnings_per_share: "$2.32",
            operating_income: "7% growth",
            gross_margin: "declined 83 basis points"
        },
        key_points: "Walmart reported strong Q4 results with sales growth across all segments. The company gained market share in grocery from higher-income households. E-commerce sales grew 27% led by store-fulfilled pickup and delivery. Walmart U.S. comp sales rose 8.3% but GM sales declined due to inflation. Operating income grew 7% but EPS declined 2.6% for the year due to charges. The company expects sales growth to slow in Q1 but increase in operating income due to lower costs. However, sales growth is expected to moderate in H2 due to difficult comps. Overall, Walmart sees uncertainty in the macro environment but remains optimistic about its long term prospects.",
        risk_and_concerns: "Concerns were raised about stubborn high inflation in dry grocery and consumables categories which could pressure customers' wallets and discretionary spending. The company also noted uncertainties in the macro environment like potential recession, lower consumer spending and income which could impact sales growth."
    }

    const style = {
        bgcolor: 'white',
        border: '2px solid #000',
        minWidth: "73vw", 
        borderRadius: "1%" 
      };

    const handleClose = () => {
        setModalOpen(false)
    }

    return (
        <Modal
        open={modalOpen}
        onClose={handleClose}
        style={{display: "flex", flexDirection:"column",alignItems:'center',justifyContent:'center', overflow: "scroll"}}
      >
        <Box style={style} bgcolor="white">
            <ModalCloseButton handleClose={handleClose}/>
            <ModalHeader data={mock_data}/>
            <ModalFinancialSummary data={mock_data}/>
            <ModalKeyPoints data={mock_data}/>
            <ModalRiskAndConcerns data={mock_data}/>
            <ModalCompareButton/>
        </Box>
      </Modal>
    )
}

export default CustomModal

