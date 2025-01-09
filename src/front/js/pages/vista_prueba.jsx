import React, { useState } from "react";
import { Card_contenor } from "../component/cards/contenedor_cards.jsx";

export const Vista_Cards = () => {
    const [filtros, setFiltros] = useState('Explorar Rutas');

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
                                            <a className="nav-link active" aria-current="page" href="#" onClick={() => setFiltros('Explorar Rutas')}>
                                                Explorar Rutas
                                            </a>
                                        </li>
                                        <li className="nav-item">
                                            <a className="nav-link" href="#" onClick={() => setFiltros('Explorar Eventos')}>
                                                Explorar Eventos
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </nav>
                    </div>
                </div>
            </div>

            <div className="container">
                {filtros === 'Explorar Rutas' ?
                    <Card_contenor />
                    :
                    <div className="text-center">
                        <h1>Eventos</h1>
                    </div>
                }
            </div>
        </div>
    );
}
