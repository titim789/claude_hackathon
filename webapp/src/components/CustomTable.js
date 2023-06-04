import { DataGrid } from '@mui/x-data-grid';
import { useState } from 'react';
import CustomModal from './CustomModal';


const CustomTable = ({data}) =>{
    const [modalOpen, setModalOpen] = useState(false)
    const [selectedRow, setSelectedRow] = useState("")

    const handleRowClick = (row) => {
        console.log(row)
        setSelectedRow(row.row)
        setModalOpen(true)
    }

    const columns = [
        { field: 'date', headerName: 'Date of Entry', width: 125 },
        { field: 'ticker', headerName: 'Ticker', width: 75 },
        { field: 'company', headerName: 'Company Name', width: 200  },
        { field: 'rating', headerName: 'Rating' },
        { field: 'title', headerName: 'Remarks', width: 600 },
    ]

    return (<div>
                <DataGrid
                    rows={data}
                    columns={columns}
                    initialState={{
                    pagination: {
                        paginationModel: { page: 0, pageSize: 5 },
                    },
                    }}
                    pageSizeOptions={[5, 10, 15]}
                    style={{width:"80vw", left:"10%", marginBottom: "55px"}}
                    onRowClick={handleRowClick}
                />
                <CustomModal data={selectedRow} modalOpen={modalOpen} setModalOpen={setModalOpen} />
            </div>
          )
}

export default CustomTable