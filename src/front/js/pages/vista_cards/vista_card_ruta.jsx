import React from "react";
import Imagen from "../../../img/testeo.jpg";
import Icon_message from "../../../img/items/comment-light.svg";
import Icon_edit from "../../../img/items/pencil-edit-02.svg";
import { Button_Blue } from "../../component/buttons/button_blue.jsx";

const Vista_Card_Ruta = () => {
    return (
        <div className="container contenedor_card">
            <div className="row">
                <div className="col-sm-6">
                    <img className="img-fluid imagen_defecto_card" src={Imagen} />
                </div>
                <div className="col-sm-6">
                    <div className="contenedor-tarjetas d-flex flex-column gap-2 justify-content-between h-100">
                        <div>
                            <div className="d-flex justify-content-between">
                                <div className="iconos d-flex md-9 gap-2">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M12.5 22C14.5767 22 16.6068 21.3842 18.3335 20.2304C20.0602 19.0767 21.406 17.4368 22.2007 15.5182C22.9954 13.5996 23.2034 11.4884 22.7982 9.45155C22.3931 7.41475 21.3931 5.54383 19.9246 4.07538C18.4562 2.60693 16.5852 1.6069 14.5484 1.20176C12.5116 0.796615 10.4004 1.00455 8.48182 1.79927C6.5632 2.59399 4.92332 3.9398 3.76957 5.66652C2.61581 7.39323 2 9.4233 2 11.5C2 13.236 2.42 14.8717 3.16667 16.3148L2 22L7.68516 20.8333C9.12716 21.5788 10.7652 22 12.5 22Z" stroke="black" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M18 7.25006C18.774 7.41006 19.359 7.67906 19.828 8.12606C21 9.24206 21 11.0381 21 14.6301C21 18.2221 21 20.0181 19.828 21.1341C18.656 22.2501 16.771 22.2501 13 22.2501H11C7.229 22.2501 5.343 22.2501 4.172 21.1341C3.001 20.0181 3 18.2221 3 14.6301C3 11.0381 3 9.24206 4.172 8.12606C4.642 7.67906 5.226 7.41006 6 7.25006M12.025 2.25006L12 14.2501M12.025 2.25006C11.8514 2.24784 11.6832 2.31021 11.553 2.42506C10.647 3.19006 9 5.17906 9 5.17906M12.025 2.25006C12.1812 2.25928 12.3297 2.32053 12.447 2.42406C13.353 3.19006 15 5.18006 15 5.18006" stroke="black" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                </div>
                                <div className="rating d-flex gap-2">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M8.23642 7.33797L1.85642 8.26297L1.74342 8.28597C1.57236 8.33138 1.41641 8.42138 1.29151 8.54677C1.16661 8.67216 1.07722 8.82846 1.03248 8.9997C0.987739 9.17093 0.989246 9.35098 1.03685 9.52144C1.08445 9.69191 1.17643 9.84668 1.30342 9.96997L5.92542 14.469L4.83542 20.824L4.82242 20.934C4.81195 21.1109 4.84868 21.2874 4.92887 21.4455C5.00905 21.6035 5.1298 21.7374 5.27875 21.8335C5.42771 21.9295 5.59951 21.9843 5.77657 21.9921C5.95363 21.9999 6.12958 21.9605 6.28642 21.878L11.9924 18.878L17.6854 21.878L17.7854 21.924C17.9505 21.989 18.1299 22.0089 18.3052 21.9817C18.4805 21.9545 18.6454 21.8812 18.783 21.7692C18.9206 21.6573 19.026 21.5107 19.0883 21.3446C19.1505 21.1785 19.1675 20.9988 19.1374 20.824L18.0464 14.469L22.6704 9.96897L22.7484 9.88397C22.8598 9.74674 22.9329 9.58242 22.9601 9.40776C22.9874 9.23311 22.9678 9.05435 22.9035 8.8897C22.8392 8.72505 22.7323 8.5804 22.5939 8.47048C22.4555 8.36056 22.2904 8.28931 22.1154 8.26397L15.7354 7.33797L12.8834 1.55797C12.8009 1.3905 12.6731 1.24948 12.5146 1.15087C12.3561 1.05226 12.1731 1 11.9864 1C11.7997 1 11.6168 1.05226 11.4582 1.15087C11.2997 1.24948 11.1719 1.3905 11.0894 1.55797L8.23642 7.33797Z" fill="#FFD700" />
                                    </svg>
                                    <h5 className="m-0">4.8</h5>
                                </div>
                            </div>
                            <div>
                                <h1 className="m-0">Bar & Pubs Route</h1>
                                <h5 className="m-0">@pepe.pe</h5>
                            </div>
                            <hr />
                            {/*<div className="d-flex flex-column">*/}
                            <div className="Rutas d-flex justify-content-between contenedores_secciones">

                                <p className="m-0">Route</p>


                                <p className="m-0">Show Route</p>

                            </div>
                            <hr />
                            <div className="Review d-flex justify-content-between contenedores_secciones">

                                <p className="m-0">Review</p>


                                <p className="m-0">Show Route</p>

                            </div>
                            <hr />
                            <div className="Comments_Reviews d-flex justify-content-between contenedores_secciones">

                                <p className="m-0">Comments & Reviews</p>


                                <p className="m-0">Show Route</p>

                            </div>
                            {/*</div>*/}
                            <hr />
                        </div>
                        <Button_Blue nombre={"Go Route"} />
                    </div>
                </div>


            </div >
        </div>

    );
};

export default Vista_Card_Ruta;
