import { useState } from 'react';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';

export default function RawForm() {
  const [rawData, setRawData] = useState('');
  const { getAccessTokenSilently } = useAuth0();

  const handleChange = (e) => setRawData(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = await getAccessTokenSilently();
      await axios.post('http://localhost:5000/submit', { data: rawData }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      alert('Submitted!');
    } catch (err) {
      console.error(err);
      alert('Submission failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        name="data"
        placeholder="Paste jumbled data here..."
        rows={10}
        cols={50}
        onChange={handleChange}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
