import React from 'react'
import { Link } from 'react-router-dom';
import { ClockCounterClockwise, Gear, List, Plus, Question, Book } from 'phosphor-react'

const Sidebar = ({ sessions, selectSession, startNewConversation }) => {

    return (
        <aside className={`sidebar-styled`}> 
            <div>
                <List weight='bold' size={20} />
                <button onClick={startNewConversation} ><Plus weight='bold' size={20}/>Novo chat</button>
            </div>
            <div className='papel' style={{height: '85%'}} >
            <ul >
            {sessions.slice().reverse().map(session => (<li key={session.session_id} onClick={() => selectSession(session.session_id)} className="item-menu"  style={{color: 'white'}} >{session.session_title ? session.session_title.substring(0, 40) : session.session_id.substring(0, 8)}  </li>
))}
            </ul>
         
            </div>
            <div className='sidebar-bottom' >
            

                <div><Book weight='bold' size={20} />
                <Link to="/rewrite"> 
                <span className="txt-link">ReprografIA</span>
                 </Link>
                </div>

                <div><ClockCounterClockwise weight='bold' size={20} />Actividad</div>

                <div><Gear weight='bold' size={20} />Configuración</div>
                <p>Code by @nilsondream</p>
            </div>
        </aside>
    )
}

export default Sidebar