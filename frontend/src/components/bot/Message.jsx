import React, { useState, memo } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { MathComponent } from 'mathjax-react';
import './Message.css';
import './bot.scss';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'phosphor-react';

const CodeBlock = memo(({ language, value }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    setCopied(true);
    setTimeout(() => setCopied(false), 2000); // Volta a exibir "Copiar código" depois de 2 segundos
  };

  return (
    <div className="code-block">
      <div className="code-header">
        <span className="language">{language}</span>
        <CopyToClipboard text={value} onCopy={handleCopy}>
          <button
            className="copy-button"
            style={{ display: 'flex' }}
            aria-label={copied ? "Código copiado" : "Copiar código"}
            aria-live="polite"
          >
            {copied ? (
              <>
                <Check weight="bold" size={18} /> Copiado
              </>
            ) : (
              <>
                <Copy weight="bold" size={18} /> Copiar código
              </>
            )}
          </button>
        </CopyToClipboard>
      </div>
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{ padding: '25px' }}
        className="codes"
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
});

const MathBlock = memo(({ formula }) => (
  <div className="math-block">
    <MathComponent tex={formula} />
  </div>
));

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
          },
          math: ({ value }) => <MathBlock formula={value} />,
          inlineMath: ({ value }) => <MathBlock formula={value} />,
        }}
      />
    </div>
  );
};

export default Message;

