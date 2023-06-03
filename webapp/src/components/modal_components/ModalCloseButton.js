import CloseIcon from '@mui/icons-material/Close'
import {IconButton} from "@mui/material"
import "./css/ModalCloseButton.css"

const ModalCloseButton = ({handleClose}) => {

    return (
        <div className='closebutton'>
            <IconButton onClick={handleClose}>
                <CloseIcon/>
            </IconButton>
        </div>
    )
}

export default ModalCloseButton