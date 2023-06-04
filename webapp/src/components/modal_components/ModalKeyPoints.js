// To-do add a card to contain the content of the key points from the management briefing

import "./css/ModalKeyPoints.css"

const ModalKeyPoints =({data}) => {
    return(
        <div className="keypoints">
            <h3>Key Points from Management Briefing</h3>
            <ul>
                {data.title?<li>{data.title}</li>:<></>}
                {data.catalyst?<li>{data.catalyst}</li>:<></>}
            </ul>
        </div>
    )
}

export default ModalKeyPoints