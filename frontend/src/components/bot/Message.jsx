import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import './Message.css';
import './bot.scss'
//import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism';
// Outros estilos:
// import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
// import { solarizeddark } from 'react-syntax-highlighter/dist/esm/styles/prism';
// import { tomorrowNight } from 'react-syntax-highlighter/dist/esm/styles/prism';
// import { monokai } from 'react-syntax-highlighter/dist/esm/styles/prism';
// import { nightOwl } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy } from 'phosphor-react';
// import { base16AteliersulphurpoolLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
// import { ayuDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
// import { gruvboxDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const CodeBlock = ({ language, value }) => {
  return (
    <div className="code-block">
      <div className="code-header" >
        <span className="language">{language}</span>
        <CopyToClipboard text={value}>
          <button className="copy-button" style={{display: 'flex'}}><Copy weight="bold" size={18} /> Copiar código</button>
        </CopyToClipboard>
      </div >
      <SyntaxHighlighter language={language} style={oneDark} customStyle={{padding: '25px'}} className='codes'>
        {value}
      </SyntaxHighlighter>
    </div>
  );
};

const Message = ({ text, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      <ReactMarkdown
        children={text}
        components={{
          code: ({ node, inline, className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <CodeBlock language={match[1]} value={String(children).replace(/\n$/, '')} />
            ) : (
              <code className={className} {...props}>
                {children}
              </code>
            );
          }
        }}
      />
    </div>
  );
};

export default Message;







