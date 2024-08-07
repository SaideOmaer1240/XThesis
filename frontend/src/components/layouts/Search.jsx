import React from 'react';
import { Image, Microphone, PaperPlaneRight } from 'phosphor-react'; 
 

const SearchInput = ({ inputValue, onInputChange, onSend, placeholder }) => {
  return (
    <div className="search-styled">
      <div>
        <button className='files'>
        <Image weight="bold" size={28} />
        </button>
      
      <textarea
          value={inputValue}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSend()}
          placeholder={placeholder || 'Ingresa una instrucción aqui'}
        />
        <button onClick={onSend} className="send-button">
          <PaperPlaneRight weight="bold" size={25} />
        </button>
        <button className='microfone'>
         <Microphone weight="bold" size={25} />
        </button>
      </div>
      <p>Es posible que IA muestre información imprecisa, incluidos datos sobre personas, por lo que debes verificar sus respuestas.</p>
    </div>
  );
};

export default SearchInput;

