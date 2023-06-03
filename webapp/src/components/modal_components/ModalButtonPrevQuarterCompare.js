//To-do Display button that allows user to compare with previous quarter's briefing

import { Button } from "@mui/material"

const ModalButtonPrevQuarterCompare = ({data}) => {

    const handleClick = () => {
        console.log(data)
    }

    return(
        <Button variant="contained" onClick={handleClick}>
            Compare to Previous Quarter
        </Button>
    )
}

export default ModalButtonPrevQuarterCompare