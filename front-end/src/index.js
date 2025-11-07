import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <Auth0Provider
    domain="your-tenant.auth0.com"
    clientId="your-client-id"
    authorizationParams={{
      redirect_uri: window.location.origin,
      audience: "https://your-api-identifier"
    }}
    cacheLocation="localstorage"
  >
    <App />
  </Auth0Provider>
);
