import React, { useEffect, useState, useContext } from "react";
import Axios from "axios";
import { ChatState } from "../context/ChatProvider";
import SideDrawer from "../components/miscellaneous/SideDrawer";
import ChatBox from "../components/miscellaneous/ChatBox";
import MyChats from "../components/miscellaneous/MyChats";
import axios from "axios";
import Rate from "../components/miscellaneous/Rating";

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

const Userpage = () => {
  const { user } = ChatState();

  const [value, setvalue] = useState("");
  const [response, setResponse] = useState("");
  const [multiResponse, setMultiResponse] = useState({});

  const handleOnchange = (val) => {
    setvalue(val);
    // console.log(typeof val);
  };

  const options = [
    { label: "English", value: "English" },
    { label: "Hindi", value: "Hindi" },
    { label: "Marathi", value: "Marathi" },
    { label: "Tamil", value: "Tamil" },
    { label: "Telugu", value: "Telugu" },
    { label: "Gujarati", value: "Gujarati" },
    { label: "Punjabi", value: "Punjabi" },
    { label: "Bengali", value: "Bengali" },
    { label: "Malyalam", value: "Malyalam" },
    { label: "Urdu", value: "Urdu" },
    { label: "Odia", value: "Odia" },
    { label: "Assamese", value: "Assamese" },
    { label: "Kannada", value: "Kannada" },
  ];

  const [textInput, setTextInput] = useState("");

  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    setTextInput(inputValue);
  };

  const handleClick = async () => {
    const formData = {
      prompt: textInput,
      language: value,
    };
    console.log(formData);

    // axios
    //   .post("http://localhost:5001/get_response", formData)
    //   .then((response) => {
    //     // console.log(response.data);
    //     setResponse(response.data);
    //   })
    //   .catch((error) => {
    //     console.log(error);
    //   });

    axios
      .post("http://localhost:7000/get_response", formData)
      .then((response) => {
        console.log(response.data);
        setMultiResponse(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    renderLawyer();
  }, [response, multiResponse]);

  const renderLawyer = () => {
    const keys = Object.keys(multiResponse);
    return (
      <>
        {keys.map((key, index) => (
          <div key={index}>
            <Box
              display="flex"
              flexDirection={"column"}
              w="90%"
              m="4"
              p="3"
              bg={"#faf5ff"}
              borderRadius={"3"}
              borderColor={"#7e22ce"}
              borderWidth={"3px"}
            >
              <Text fontSize={"xl"} fontWeight={"bold"} color="black">
                {key}
              </Text>
              <Text fontSize={"md"} color="gray">
                {multiResponse[key]}
              </Text>
              <Rate></Rate>
            </Box>
          </div>
        ))}
      </>
    );
  };

  const [audioBlob, setAudioBlob] = useState(null);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const handleStartRecording = () => {
    setRecording(true);
    // setTranslated(""); // Clear previous translation if any

    // Start recording audio
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        const recorder = new MediaRecorder(stream);
        setMediaRecorder(recorder); // Set mediaRecorder in state

        const audioChunks = [];

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        recorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          setAudioBlob(audioBlob);
        };

        recorder.start();
      })
      .catch((error) => console.error("Error:", error));
  };

  const handleStopRecording = () => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const sendAudioToAPI = async () => {
    // Make the function async
    if (audioBlob) {
      const formData = new FormData();
      formData.append("file", audioBlob, "audio.wav");

      const response = await fetch("http://localhost:7000/get_audio_response", {
        method: "POST",
        body: formData,
      });

     const data = await response.json(); // Parse the response data as JSON

      console.log(data); // Check the received data in the console

      // Now you can use the received data
      setMultiResponse(data);
      }
    }
 

  return (
    <>
      <div style={{ width: "100%" }}>
        {user && <SideDrawer />}
        <Box
          display="flex"
          w="100%"
          h="93%"
          alignItems={"center"}
          className="court"
          justifyContent={"center"}
        >
          <Box
            display="flex"
            flexDirection={"column"}
            justifyContent={"center"}
            // alignItems={"flex-start"}
            w="60%"
            h="91.5vh"
            p="10px"

            // bg={"#e2e8f0"}
          >
            <Box
              display="flex"
              flexDirection={"column"}
              justifyContent="center"
              alignItems={"center"}
              // bg={"white"}
              w="100%"
              h="85%"
              p="10px"
            >
              <Box display="flex">
                <Box
                  display="flex"
                  m="30"
                  alignItems={"center"}
                  // borderColor={"#7e22ce"}
                  // borderWidth={"1px"}
                  p="5"
                >
                  <Text
                    fontSize={"xl"}
                    color="white"
                    textAlign={"center"}
                    mr={"10"}
                  >
                    Please select the languages you speak:
                  </Text>

                  <MultiSelect
                    className="multi-select"
                    onChange={handleOnchange}
                    options={options}
                    backgroundColor="white"
                  />
                </Box>
              </Box>

              <Textarea
                value={textInput}
                onChange={handleInputChange}
                placeholder="Tell us about your case and requirements.."
                size="lg"
                height="200px"
                width="700px"
                mt="5px"
                mb="5px"
                borderColor={"#7e22ce"}
                borderWidth={"5px"}
                backgroundColor={"white"}
                className="textarea"
              />
              <Box display={"flex"} justifyContent={"flex-end"} w="88%">
                <button className="button" onClick={handleClick}>
                  Submit
                </button>
              </Box>
              <Box
                display="flex"
                flexDirection={"column"}
                justifyContent="center"
                alignItems={"center"}
                w="100%"
                h="20%"
                // p="20"
                mt="10"
              >
                <Box display="flex" w="75%" alignItems={"flex-start"}>
                  <Text fontSize={"xl"} color="white" alignSelf={"left"} mb="2">
                    Enter Audio Input:
                  </Text>
                </Box>

                <ButtonGroup gap="4">
                  <button
                    className="button"
                    onClick={handleStartRecording}
                    disabled={recording}
                  >
                    {recording ? "Recording..." : "Start Recording"}
                    {/* Start Recording */}
                  </button>
                  <button
                    className="button"
                    onClick={handleStopRecording}
                    disabled={!recording}
                  >
                    Stop Recording
                  </button>
                  <button
                    className="button"
                    onClick={sendAudioToAPI}
                    disabled={!audioBlob}
                  >
                    Send Audio
                  </button>
                </ButtonGroup>
              </Box>
            </Box>
          </Box>
          <Box
            display="flex"
            flexDirection={"column"}
            alignItems={"center"}
            w="39%"
            h="88.5vh"
            // bg={"white"}
          >
            <Text
              fontSize={"lg"}
              fontWeight={"bold"}
              color="white"
              m="5"
              mb="0"
              p="3"
              borderColor={"#7e22ce"}
              borderWidth={"3px"}
            >
              Recommended Lawyers
            </Text>
            <Box overflowY={"auto"} mt="5">
              {multiResponse ? renderLawyer() : ""}
            </Box>
          </Box>
        </Box>
      </div>
    </>
  );
};

export default Userpage;
