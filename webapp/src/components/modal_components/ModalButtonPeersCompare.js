//To-do Display button to allow user to compare to peers

import { Button } from "@mui/material"

const ModalButtonPeersCompare = ({setComparing}) => {

    const handleClick = () => {
        setComparing(true)
    }

    return(
        <Button variant="contained" onClick={handleClick}>
            Compare to Peers
        </Button>
    )
}

export default ModalButtonPeersCompare