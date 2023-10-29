import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { ChatState } from "../context/ChatProvider";
import SideDrawer from "../components/miscellaneous/SideDrawer";

import {
  Box,
  Text,
  Radio,
  RadioGroup,
  Stack,
  Textarea,
  Button,
  ButtonGroup,
} from "@chakra-ui/react";
import MultiSelect from "react-multiple-select-dropdown-lite";
import "react-multiple-select-dropdown-lite/dist/index.css";
import "./styles.css";
import { useToast } from "@chakra-ui/react";

const Adminpage = () => {
  const { user } = ChatState();

  const [file, setFile] = useState(null);
  const toast = useToast();

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleClick = async () => {
    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("http://localhost:7000/update_db", formData)
      .then((response) => {
        console.log(response.json);
        if (response.ok) {
          console.log(response);
          toast({
            title: "Upload Successful!",
            status: "success",
            duration: 3000,
            isClosable: true,
            position: "bottom",
          });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <>
      <div style={{ width: "100%" }}>
        <div style={{ width: "100%" }}>{user && <SideDrawer />}</div>
        <Box display={"flex"} justifyContent={"center "} m={"10"}>
          <input type="file" onChange={handleFileUpload} />
          <Button onClick={handleClick}>Upload</Button>
        </Box>
        <Box>
          <iframe
            title="Tableau Dashboard"
            src="https://public.tableau.com/views/Lawyer_Dashboard2/Dashboard2?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
            width="800"
            height="600"
          />
        </Box>
      </div>
    </>
  );
};

export default Adminpage;
