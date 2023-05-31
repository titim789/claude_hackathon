import {Button, Box, Modal, Typography, Card, CardContent} from "@mui/material"

const CustomModal = ({data, modalOpen, setModalOpen}) => {

    const style = {
        bgcolor: 'white',
        border: '2px solid #000',
      };

    const handleClose = () => {
        setModalOpen(false)
    }

    return (
        <Modal
        open={modalOpen}
        onClose={handleClose}
        style={{display: "flex", flexDirection:"column",alignItems:'center',justifyContent:'center'}}
      >
        <Box display="flex" sx={{justifyContent:"center"}} style={style} bgcolor="white">
            <Card sx={{ minWidth: "80vw"}}>
                <CardContent>
                    <Typography variant="h5" display="flex" justifyContent="center">
                        {data.name}
                    </Typography>
                    <Typography variant="body2" display="flex" justifyContent="center">
                        {data.age}
                    </Typography>
                </CardContent>
            </Card>
        </Box>
      </Modal>
    )
}

export default CustomModal

