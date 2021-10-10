import React from 'react';
import Logo from '../../Logo';
import './Login.css';
import useMultipleRefs from '../../../hooks/useMultipleRefs';
import { useUserContext } from '../../../contexts/UserContext/UserContext';

const LoginForm = (/* { logIn } */) => {
  const { refs, onChange } = useMultipleRefs(['email', 'password']);
  const { useAuth: { logIn } } = useUserContext();

  const handleSubmit = (e) => {
    e.preventDefault();
    logIn({ email: refs.email, password: refs.password });
  };

  return (
    <div className="main">
      <section className="main-section">
        <div className="container">
          <div className="contents">
            <div className="w-50">
              <div className="fb-logo-items">
                <div className="fb-logo">
                  <Logo />
                </div>
              </div>
            </div>

            <div className="w-50">
              <div className="login-form">
                <div className="log-content">
                  <form onSubmit={handleSubmit} autoComplete="true">
                    <label htmlFor="email">
                      Email
                      <input
                        type="email"
                        name="email"
                        autoComplete="email"
                        ref={refs.email}
                        onChange={onChange}
                      />
                    </label>

                    <label htmlFor="password">
                      Password
                      <input
                        type="password"
                        name="password"
                        autoComplete="current-password"
                        ref={refs.password}
                        onChange={onChange}
                      />
                    </label>
                    <input type="submit" />
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};

export default LoginForm;
