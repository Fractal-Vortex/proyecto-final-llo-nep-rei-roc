import React from "react";
import imagen from "../../../img/testeo.jpg";
import Mark from "../../../img/items/mark.png";

export const Card_Ruta = () =>{

    return(
    <div className="card" style={{width: "18rem", padding:6}}>
        <img src={imagen} className="card-img-top" alt="..." style={{ margin: 1, borderRadius: "8px" }} />
        <div className="card-body text-start">
          <h5 className="card-title">Bar & Pubs Route</h5>
          <p className="card-text">@pepe</p>
          <div className="d-flex justify-content-end">
            <p className="card-text">⭐4,8</p>
          </div>
        </div>
        <div className="Mark_tarjeta position-absolute" style={{ top: 13, right: 10 }}>
          <img src={Mark} width={40} height={40}/>
        </div>
    </div>
    )

}