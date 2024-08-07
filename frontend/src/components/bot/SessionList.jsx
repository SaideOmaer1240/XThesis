import React from 'react';

const SessionList = ({ isSidebarOpen, sessions, selectSession, startNewConversation }) => {
    return (
        <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
            <div className='papel' style={{height: '85%'}}>
            <ul >
            {sessions.slice().reverse().map(session => (<li key={session.session_id} onClick={() => selectSession(session.session_id)} className="item-menu">{session.session_title ? session.session_title.substring(0, 50) : session.session_id.substring(0, 8)}</li>
))}
            </ul>
         
            </div>
            
            <button
                onClick={startNewConversation}
                style={{ padding: '10px', borderRadius: '5px', backgroundColor: '#f44336', color: 'white' }}
            >
                Start New Conversation
            </button>
            </aside>
    );
};

export default SessionList;
