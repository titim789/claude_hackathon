// To-do add a card to contain the content of the key points from the management briefing

import "./css/ModalKeyPoints.css"

const ModalKeyPoints =({data}) => {
    return(
        <div className="keypoints">
            <h3>Key Points from Management Briefing:</h3>
            <p>{data.key_points}</p>
        </div>
    )
}

export default ModalKeyPoints