import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import {IconButton} from "@mui/material"
import "./css/ModalBackButton.css"

const ModalBackButton = ({handleBack}) => {

    return (
        <div className='backbutton'>
            <IconButton onClick={handleBack}>
                <ArrowBackIcon/>
            </IconButton>
        </div>
    )
}

export default ModalBackButton