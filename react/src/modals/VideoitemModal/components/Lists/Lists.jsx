import React, { useState } from 'react';
import axios from 'axios';
import { useVideoitemContext } from '../../context/context';
import urls from '../../../../dev_urls';

const Lists = () => {
  const { videoitemId, userLists } = useVideoitemContext();

  console.log('lists', userLists);

  const [state, setState] = useState({
    userId: '',
    listId: '',
  });

  const handleChange = (evt) => {
    const { value, name } = evt.target;
    setState((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const addToList = async () => {
    const request = {
      list_id: state.listId,
      user_id: state.userId,
      videoitems: [videoitemId],
    };

    const url = `${urls.API_BASE}${state.userId}/lists/${state.listId}/add/`;

    const { data } = await axios.post(url, request);

    console.log('data', data);
  };

  return (
    <>
      <form>
        <label htmlFor="userId">
          user_id
          <input
            type="text"
            name="userId"
            value={state.userId}
            onChange={handleChange}
          />
        </label>
        <br />
        <label htmlFor="listId">
          list_id
          <input
            type="text"
            name="listId"
            value={state.listId}
            onChange={handleChange}
          />
        </label>
      </form>
      <button type="button" onClick={addToList}>
        Legg til i liste
      </button>
    </>
  );
};

export default Lists;
