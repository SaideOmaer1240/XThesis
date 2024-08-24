import React, { useState, useEffect, useRef } from 'react';
import { Image, Microphone, PaperPlaneRight } from 'phosphor-react';

const SearchInput = ({ inputValue, onInputChange, onSend, placeholder }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);

  const handleImageUpload = (event) => {
    setSelectedImage(event.target.files[0]);
    onInputChange("Analisando a imagem"); // Exibe a mensagem ao selecionar uma imagem
  };

  const handleSend = () => {
    onSend(inputValue, selectedImage, audioBlob);
    setSelectedImage(null);
    setAudioBlob(null);
  };

  const handleAudioStartStop = () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          setAudioBlob(event.data);
          onInputChange("Analisando áudio"); // Exibe a mensagem ao gravar um áudio
        };

        mediaRecorder.start();
        setIsRecording(true);
      });
    }
  };

  useEffect(() => {
    if (audioBlob) {
      handleSend(); // Envia automaticamente o áudio
    }
  }, [audioBlob]);

  return (
    <div className="search-styled">
      <div>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          style={{ display: 'none' }}
          id="upload-image"
        />
        <label htmlFor="upload-image" className="files">
          <Image weight="bold" size={28} />
        </label>

        <textarea
          value={inputValue}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={placeholder || 'Digite sua mensagem aqui'} 
        />

        <button onClick={handleSend} className="send-button">
          <PaperPlaneRight weight="bold" size={25} />
        </button>

        <button onClick={handleAudioStartStop} className="microfone">
          <Microphone weight="bold" size={25} />
          {isRecording ? 'Parar' : 'Gravar'}
        </button>
      </div>

      {selectedImage && <p>Imagem selecionada: {selectedImage.name}</p>}
      <p>Es posible que IA muestre información imprecisa, incluidos datos sobre personas, por lo que debes verificar sus respuestas.</p>
    </div>
  );
};

export default SearchInput;

