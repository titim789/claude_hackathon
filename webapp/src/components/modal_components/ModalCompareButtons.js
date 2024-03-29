import { Stack } from "@mui/material"
import ModalButtonPrevQuarterCompare from "./ModalButtonPrevQuarterCompare"
import ModalButtonPeersCompare from "./ModalButtonPeersCompare"


const ModalCompareButton = ({setComparing}) => {

    return (
        <Stack spacing={2} direction="row" style={{padding: "2%"}}>
            {/* <ModalButtonPrevQuarterCompare data={"PREV_QUARTER_DATA"}/> */}
            <ModalButtonPeersCompare setComparing={setComparing}/>
        </Stack>
    )
}

export default ModalCompareButton