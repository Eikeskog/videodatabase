import React, { useState } from 'react';
import { useVideoitemContext } from '../../context/context';
import { useUserContext } from '../../../../common/contexts/UserContext/UserContext';
import urls from '../../../../dev_urls';

// not implemented
const Lists = () => {
  const { videoitemId/* , userLists */ } = useVideoitemContext();
  const {
    useAuth: {
      user: { id: userId },
    },
    useAuthorizedFetch: {
      authorizedFetch,
    },
  } = useUserContext();

  const [state, setState] = useState({
    userId: '',
    listId: '',
    newListLabel: '',
  });

  const handleChange = (evt) => {
    const { value, name } = evt.target;
    setState((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleResponse = (data) => {
    console.log(data);
  };

  const handleError = (error) => {
    console.log(error);
  };

  const addToList = async () => {
    const request = {
      list_id: state.listId,
      user_id: state.userId,
      videoitems: [videoitemId],
    };

    const url = `${urls.API_BASE}${userId}/lists/${state.listId}/add/`;

    authorizedFetch({
      method: 'post',
      url,
      handleResponse,
      handleError,
      body: request,
    });
  };

  const newList = async () => {
    const url = `${urls.API_BASE}${userId}/lists/new/${state.newListLabel}/`;

    const request = {
      list_label: state.newListLabel,
      user_id: userId,
      videoitems: [videoitemId],
    };

    authorizedFetch({
      method: 'post',
      url,
      handleResponse,
      handleError,
      body: request,
    });
  };

  const testAllUserLists = async () => {
    const url = `${urls.API_BASE}${userId}/lists/`;

    authorizedFetch({
      method: 'get',
      url,
      handleResponse,
      handleError,
      // body: request,
    });
    // api/<int:user_id>/lists/
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
      <form>
        <label htmlFor="newListLabel">
          newListLabel
          <input
            type="text"
            name="newListLabel"
            value={state.newListLabel}
            onChange={handleChange}
          />
        </label>
      </form>
      <button type="button" onClick={newList}>
        Lag ny liste
      </button>
      <p role="presentation" onClick={testAllUserLists}>test all userlists</p>
    </>
  );
};

export default Lists;
