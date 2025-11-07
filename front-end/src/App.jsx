import { useAuth0 } from '@auth0/auth0-react';
import RawForm from './components/RawForm';

export default function App() {
  const { loginWithRedirect, logout, isAuthenticated, isLoading, user } = useAuth0();

  if (isLoading) return <div>Loading...</div>;

  const roles = user?.["https://your-app.com/roles"] || [];

  return (
    <div>
      <h1>SMTP Validator</h1>
      {!isAuthenticated ? (
        <button onClick={() => loginWithRedirect()}>Login</button>
      ) : (
        <>
          <p>Welcome, {user.name}</p>
          {roles.includes("admin") && <p>You have admin access</p>}
          <button onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>
            Logout
          </button>
          <RawForm />
        </>
      )}
    </div>
  );
}
