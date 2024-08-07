import React from 'react';
import Sidebar from '../../components/layouts/Sidebar';
import Home from './Home';
import '../../styles/styles/Global.scss';

const ChatBot = () => {
    return (
        <div className='app-styled'>
            <Sidebar />
            <Home />
        </div>
    );
};

export default ChatBot;
