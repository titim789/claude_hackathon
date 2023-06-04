
import { getComparePeers } from "../../api/api"
import { useState, useEffect } from "react"
import "./css/ModalCompareContent.css"

const ModalCompareContent = ({comparedValue, show}) => {

    const [comparedData,setComparedData] = useState([])
    const [isLoading, setIsLoading] = useState(false)

    useEffect(()=>{
        updateCompareData()
    },[comparedValue])

    const updateCompareData = async () => {
        setIsLoading(true)
        await getComparePeers()
            .then( (data) => {
                setComparedData(data.data)
                console.log(data)
                setIsLoading(false)
            }
            )
            .catch((e)=>{console.log(e)})
    }
    
    console.log(comparedData)

    return (
        <div className="modalcomparecontent">
            {
                show?
                isLoading?<div>Loading...</div>:
                <div className="modalcomparedetails">
                    <div className="company1">
                        <h3>{comparedData?comparedData.company1:null}</h3>
                        <h4>Challenges</h4>
                        {comparedData?comparedData.challenges.Amazon:null}
                        <h4>Financial</h4>
                        {comparedData?comparedData.financials.Amazon:null}
                        <h4>Growth</h4>
                        {comparedData?comparedData.growth.Amazon:null}
                        <h4>Insider</h4>
                        {comparedData?comparedData.insider.Amazon:null}
                        <h4>Leadership</h4>
                        {comparedData?comparedData.leadership.Amazon:null}
                        <h4>Resilience</h4>
                        {comparedData?comparedData.resilience.Amazon:null}
                    </div>
                    <div className="company2">
                        <h3>{comparedData?comparedData.company2:null}</h3>
                        <h4>Challenges</h4>
                        {comparedData?comparedData.challenges["Home Depot"]:null}
                        <h4>Financial</h4>
                        {comparedData?comparedData.financials["Home Depot"]:null}
                        <h4>Growth</h4>
                        {comparedData?comparedData.growth["Home Depot"]:null}
                        <h4>Insider</h4>
                        {comparedData?comparedData.insider["Home Depot"]:null}
                        <h4>Leadership</h4>
                        {comparedData?comparedData.leadership["Home Depot"]:null}
                        <h4>Resilience</h4>
                        {comparedData?comparedData.resilience["Home Depot"]:null}
                    </div>
                </div>:
                <></>
            }
        </div>
    )
}

export default ModalCompareContent