import {TableContainer, Paper, TableCell, TableHead, Table, TableRow, TableBody, Checkbox}  from '@mui/material';
import { useState } from 'react';
import CustomModal from './CustomModal';


const CustomTable = ({columns, data}) =>{

    const [checked, setChecked] = useState(Array.from({ length: data.length }, () => false));
    const [checkedData, setCheckedData] = useState([])
    const [headerChecked, setHeaderChecked] = useState(false)
    const [modalOpen, setModalOpen] = useState(false)
    const [selectedRow, setSelectedRow] = useState("")

    const handleCheck = (e, row, index) => {
        checked[index] = e.target.checked
        if (e.target.checked) {
            setCheckedData([...checkedData, row]);
        } else {
            setHeaderChecked(false)
            setCheckedData(checkedData.filter(r => r !== row));
        }
    }

    const handleHeaderCheck= (e) => {
        setHeaderChecked(e.target.checked);
        setChecked(Array.from({ length: data.length }, () => e.target.checked))
        console.log(e.target.checked)
        if (e.target.checked) {
            setCheckedData(data);
        } else {
            setCheckedData([]);
        }
    }

    const handleRowClick = (row) => {
        console.log(row)
        setSelectedRow(row)
        setModalOpen(true)
    }


    return (<div><TableContainer component={Paper} style={{width: "80vw", margin:"auto"}}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell padding='checkbox'><Checkbox checked={headerChecked} onChange={handleHeaderCheck}/></TableCell>
                  <TableCell >Name</TableCell>
                  <TableCell>Age</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {
                    data.map((row,index) => (
                        <TableRow key={row.name}>
                            <TableCell>
                            <Checkbox checked={checked[index]} onChange={(e) => handleCheck(e, row, index)} />
                            </TableCell>
                            <TableCell onClick = {()=>handleRowClick(row)}>
                                {row.name}
                            </TableCell>
                            <TableCell onClick = {()=>handleRowClick(row)}>
                                {row.age}
                            </TableCell>
                        </TableRow>
                    ))
                }
              </TableBody>
            </Table>
          </TableContainer>
          <CustomModal data={selectedRow} modalOpen={modalOpen} setModalOpen={setModalOpen} />
          </div>
          )
}

export default CustomTable