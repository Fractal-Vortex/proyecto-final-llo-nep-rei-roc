import React from "react";
import { Card_Ruta } from "./card_ruta.jsx";

export const Card_contenor = () => {
    return (
        <div>
            <div className="container mb-4">
                <div className="row justify-content-center">
                    <div className="col-md-9">
                        <nav className="navbar navbar-expand-lg bg-body-tertiary justify-content-center">
                            <div className="container-fluid">
                                <div className="collapse navbar-collapse" id="navbarNav">
                                    <ul className="navbar-nav">
                                        <li className="nav-item">
                                            <a className="nav-link active" aria-current="page" href="#">All</a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link" href="#">Popular</a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link" href="#">Recommended</a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link" href="#">Most Viewed</a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link" href="#">Others</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </nav>
                    </div>
                </div>
            </div>
            <div className="container">
                <div className="row justify-content-center mb-4">
                    <div className="col-md-3 d-flex justify-content-center">
                        <Card_Ruta />
                    </div>
                    <div className="col-md-3 d-flex justify-content-center">
                        <Card_Ruta />
                    </div>
                    <div className="col-md-3 d-flex justify-content-center">
                        <Card_Ruta />
                    </div>
                </div>
                <div className="row justify-content-center mb-4">
                    <div className="col-md-3 d-flex justify-content-center">
                        <Card_Ruta />
                    </div>
                    <div className="col-md-3 d-flex justify-content-center">
                        <Card_Ruta />
                    </div>
                    <div className="col-md-3 d-flex justify-content-center">
                        <Card_Ruta />
                    </div>
                </div>
            </div>
        </div>
    );
}
