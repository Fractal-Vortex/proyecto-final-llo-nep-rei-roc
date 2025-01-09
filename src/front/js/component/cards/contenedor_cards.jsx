import React, { useRef } from "react";
import { Card_Ruta } from "./card_ruta.jsx";

export const Card_contenor = () => {
    const scrollRef = useRef(null);

    const scrollLeft = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollBy({ left: -300, behavior: 'smooth' });
        }
    };

    const scrollRight = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollBy({ left: 300, behavior: 'smooth' });
        }
    };

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
            <div className="d-none d-md-block">
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
            <div className="d-md-none slider-container">
                <button className="scroll-btn left" onClick={scrollLeft}>&#10094;</button>
                <div className="card-slider" ref={scrollRef}>
                    <div className="card-item"><Card_Ruta /></div>
                    <div className="card-item"><Card_Ruta /></div>
                    <div className="card-item"><Card_Ruta /></div>
                    <div className="card-item"><Card_Ruta /></div>
                    <div className="card-item"><Card_Ruta /></div>
                    <div className="card-item"><Card_Ruta /></div>
                </div>
                <button className="scroll-btn right" onClick={scrollRight}>&#10095;</button>
            </div>
        </div>
    );
}
