//To-do Display button to allow user to compare to peers

import { Button } from "@mui/material"

const ModalButtonPeersCompare = ({data}) => {

    const handleClick = () => {
        console.log(data)
    }

    return(
        <Button variant="contained" onClick={handleClick}>
            Compare to Peers
        </Button>
    )
}

export default ModalButtonPeersCompare