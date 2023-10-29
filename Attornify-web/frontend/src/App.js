import "./App.css";
import { Route } from "react-router-dom";
import Homepage from "./Pages/Homepage";
import Userpage from "./Pages/Userpage";
import Adminpage from "./Pages/AdminPage";

function App() {
  return (
    <div className="App">
      <Route path="/" component={Homepage} exact></Route>
      <Route path="/user" component={Userpage}></Route>
      <Route path="/admin" component={Adminpage}></Route>
    </div>
  );
}

export default App;
