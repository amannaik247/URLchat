import logo from './logo.svg';
import './App.css';
import QuestionForm from './QuestionForms';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Welcome to URLchat!
        </p>
        <QuestionForm />
      </header>
    </div>
  );
}

export default App;
