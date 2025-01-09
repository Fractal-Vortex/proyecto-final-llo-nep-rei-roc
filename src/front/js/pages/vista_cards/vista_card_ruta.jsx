import React from "react";
import Imagen from "../../../img/testeo.jpg";
import Icon_message from "../../../img/items/comment-light.svg"
import Icon_edit from "../../../img/items/pencil-edit-02.svg"

const Vista_Card_Ruta = () => {
    return (
        <div className="container-fluid d-flex">
            <img src={Imagen} width={"700px"} height={"660px"} style={{ borderRadius: "8px" }} />
            <div className="ms-5 contenedor-tarjetas">
                <div className="d-flex justify-content-between">
                    <div className="iconos d-flex md-9">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12.5 22C14.5767 22 16.6068 21.3842 18.3335 20.2304C20.0602 19.0767 21.406 17.4368 22.2007 15.5182C22.9954 13.5996 23.2034 11.4884 22.7982 9.45155C22.3931 7.41475 21.3931 5.54383 19.9246 4.07538C18.4562 2.60693 16.5852 1.6069 14.5484 1.20176C12.5116 0.796615 10.4004 1.00455 8.48182 1.79927C6.5632 2.59399 4.92332 3.9398 3.76957 5.66652C2.61581 7.39323 2 9.4233 2 11.5C2 13.236 2.42 14.8717 3.16667 16.3148L2 22L7.68516 20.8333C9.12716 21.5788 10.7652 22 12.5 22Z" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M18 7.25006C18.774 7.41006 19.359 7.67906 19.828 8.12606C21 9.24206 21 11.0381 21 14.6301C21 18.2221 21 20.0181 19.828 21.1341C18.656 22.2501 16.771 22.2501 13 22.2501H11C7.229 22.2501 5.343 22.2501 4.172 21.1341C3.001 20.0181 3 18.2221 3 14.6301C3 11.0381 3 9.24206 4.172 8.12606C4.642 7.67906 5.226 7.41006 6 7.25006M12.025 2.25006L12 14.2501M12.025 2.25006C11.8514 2.24784 11.6832 2.31021 11.553 2.42506C10.647 3.19006 9 5.17906 9 5.17906M12.025 2.25006C12.1812 2.25928 12.3297 2.32053 12.447 2.42406C13.353 3.19006 15 5.18006 15 5.18006" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                    </div>
                    <div className="rating d-flex">
                        <h3>Hello</h3>
                    </div>
                </div>
                <h1>Bar & Pubs Route</h1>
                <h5>@pepe.pe</h5>
                <div className="mt-5">
                    <div className="Rutas border-top border-bottom d-flex justify-content-between" width={"100%"} height={"auto"}>
                        <div>
                            <p className="mt-2">Route</p>
                        </div>
                        <div>
                            <p className="mt-2">Show Route</p>
                        </div>
                    </div>
                    <div className="Review border-top border-bottom d-flex justify-content-between" width={"100%"} height={"auto"}>
                        <div>
                            <p className="mt-2">Review</p>
                        </div>
                        <div>
                            <p className="mt-2">Show Route</p>
                        </div>
                    </div>
                    <div className="Comments_Reviews border-top border-bottom d-flex justify-content-between" width={"100%"} height={"auto"}>
                        <div>
                            <p className="mt-2">Comments & Reviews</p>
                        </div>
                        <div>
                            <p className="mt-2">Show Route</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Vista_Card_Ruta;
