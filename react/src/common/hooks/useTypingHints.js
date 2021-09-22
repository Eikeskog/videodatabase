import { useRef, useState } from 'react';
import axios from 'axios';

const useTypingHints = (itemType) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [results, setResults] = useState([]);

  const ref = useRef();

  const fetch = async () => {
    const url = `http://localhost:8000/api/typinghints/${itemType}/?s=${ref?.current?.value}`;

    const { data } = await axios.get(url);
    setResults(() => data && data);
    setIsLoading(false);
  };

  const onChange = () => {
    if (!ref?.current?.value) {
      setIsTyping(false);
      setIsLoading(false);
      return;
    }
    setIsTyping(true);
    setIsLoading(true);
    fetch();
  };

  const resetHints = () => {
    setIsTyping(false);
    setIsLoading(false);
    setResults([]);
  };

  return {
    ref,
    isTyping,
    onChange,
    results,
    isLoading,
    resetHints,
  };
};

export default useTypingHints;
