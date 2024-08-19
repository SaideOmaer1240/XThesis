import React from 'react';
import './LoadingAnimation.scss';

const LoadingAnimation = () => {
    return (
        <div className="loading-container">
            <div className="loading-circle"></div>
            <div className="loading-text">Carrgado...aguarde alguns segundos!</div>
        </div>
    );
}

export default LoadingAnimation;
