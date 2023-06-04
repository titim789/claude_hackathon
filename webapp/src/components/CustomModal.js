import { useState } from "react";
import {Box, Modal} from "@mui/material"
import ModalHeader from "./modal_components/ModalHeader";
import ModalFinancialSummary from "./modal_components/ModalFinancialSummary";
import ModalKeyPoints from "./modal_components/ModalKeyPoints";
import ModalRiskAndConcerns from "./modal_components/ModalRiskAndConcerns";
import ModalCloseButton from "./modal_components/ModalCloseButton";
import ModalCompareButton from "./modal_components/ModalCompareButtons";
import ModalPrevQuarterCompare from "./modal_components/ModalPrevQuarterCompare"
import ModalCompareHeader from "./modal_components/ModalCompareHeader";
import ModalBackButton from "./modal_components/ModalBackButton";
import ModalCompareContent from "./modal_components/ModalCompareContent";


const CustomModal = ({data, modalOpen, setModalOpen}) => {

    const [comparing, setComparing] = useState(false)
    const [compareValue, setCompareValue] = useState("")
    const [compared, setCompared] = useState(false)

    const style = {
        bgcolor: 'white',
        border: '2px solid #000',
        maxWidth: "73vw", 
        borderRadius: "1%" 
      };

    const handleClose = () => {
        setModalOpen(false)
        setComparing(false)
        setCompared(false)
    }

    const handleBack = () => {
      setComparing(false)
      setCompareValue("")
      setCompared(false)
    }

    return (
        <Modal
        open={modalOpen}
        onClose={handleClose}
        style={{ overflowY: "scroll", maxHeight: "70vh", borderRadius: "1%", left:"12.5%", top:"15%" }}
      >
        {comparing?
        <Box style={style} bgcolor="white">
          <ModalBackButton handleBack={handleBack}/>
          <ModalCompareHeader setCompareValue={setCompareValue} setCompared={setCompared} comparer={data.company}/>
          <ModalCompareContent compareValue={compareValue} show={compared}/>
        </Box>:
        <Box style={style} bgcolor="white">
            <ModalCloseButton handleClose={handleClose}/>
            <ModalHeader data={data}/>
            <ModalFinancialSummary data={data}/>
            <ModalKeyPoints data={data}/>
            <ModalRiskAndConcerns data={data}/>
            <ModalPrevQuarterCompare data={data}/>
            <ModalCompareButton setComparing={setComparing}/>
        </Box>
        }
      </Modal>
    )
}

export default CustomModal

