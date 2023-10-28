import "./App.css";
import { Route } from "react-router-dom";
import Homepage from "./Pages/Homepage";
import Userpage from "./Pages/Userpage";

function App() {
  return (
    <div className="App">
      <Route path="/" component={Homepage} exact></Route>
      <Route path="/chats" component={Userpage}></Route>
    </div>
  );
}

export default App;
