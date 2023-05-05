import { useState } from 'react';
import axios from 'axios';
function App() {
  const [contacts, setContacts] = useState([]);
  const [fullname, setFullName] = useState('');
  const [phone_number, setPhoneNumber] = useState('');
  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/phonebook/add', {
        fullname,
        phone_number,
      });
      setContacts([...contacts, response.data]);
      setFullName('');
      setPhoneNumber('');
    } catch (error) {
      console.error(error);
    }
  };
  const handleGetContacts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/phonebook');
      setContacts(response.data);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <div className="App">
      <div>
        <label htmlFor="fullname">Full Name:</label>
        <input
          type="text"
          id="fullname"
          value={fullname}
          onChange={(e) => setFullName(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="phone_number">Phone Number:</label>
        <input
          type="text"
          id="phone_number"
          value={phone_number}
          onChange={(e) => setPhoneNumber(e.target.value)}
        />
      </div>
      <button onClick={handleSubmit}>Save</button>
      <button onClick={handleGetContacts}>Get Contacts</button>
      <table>
        <thead>
          <tr>
            <th>Full Name</th>
            <th>Phone Number</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map((contact, index) => (
            <tr key={index}>
              <td>{contact.fullname}</td>
              <td>{contact.phone_number}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default App;