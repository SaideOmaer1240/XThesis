import React from 'react';
import { Image, Microphone } from 'phosphor-react';  

const SearchInput = ({ inputValue, onInputChange, onSend, placeholder }) => {
  return (
    <div className="search-styled">
      <div>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSend()}
          placeholder={placeholder || 'Ingresa una instrucción aqui'}
        />
        <Image weight="bold" size={25} />
        <Microphone weight="bold" size={25} />
      </div>
      <p>Es posible que IA muestre información imprecisa, incluidos datos sobre personas, por lo que debes verificar sus respuestas.</p>
    </div>
  );
};

export default SearchInput;
