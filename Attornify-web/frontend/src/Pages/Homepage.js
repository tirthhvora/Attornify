import React, { useEffect } from "react";
import { useHistory } from "react-router-dom";
import {
  Container,
  Box,
  Text,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Image,
} from "@chakra-ui/react";
import Login from "../components/Authentication/Login";
import SignUp from "../components/Authentication/SignUp";
import AdminLogin from "../components/Authentication/AdminLogin";
import { ReactComponent as Svg } from "../components/miscellaneous/Lawyer-pana.svg";

//import { ReactComponent as Svg } from "../components/6770876.svg";

const Homepage = () => {
  const history = useHistory();
  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("userInfo"));

    if (user) {
      console.log(user);
      history.push("/user");
    }
  }, [history]);
  return (
    // <Container maxW="xl" centerContent display="flex">
    <>
      <Box
        display="flex"
        flexDirection={"column"}
        justifyContent={"center"}
        p={1}
        // bg={"white"}
        borderRadius={"lg"}
        borderWidth={"1px"}
        w="80%"
        m={20}
        // m="40px 0 15px 0"
      >
        <Text fontSize={"5xl"} color="white" textAlign={"center"}>
          ATTORNIFY
        </Text>
        <Text fontSize={"md"} color="white" textAlign={"center"} mb="30">
          Connecting You to Legal Excellence, Effortlessly.
        </Text>
        <Svg width="600px" height="300px" />
      </Box>
      <Box
        w="100%"
        display="flex"
        alignItems={"center"}
        justifyContent={"center"}
      >
        <Box
          p={4}
          bg={"#f9fafb"}
          borderRadius={"lg"}
          borderWidth={"1px"}
          w="80%"
          display="flex"
          flexDirection={"column"}
          justifyContent={"center"}
        >
          <Tabs variant="soft-rounded" colorScheme="purple">
            <TabList mb="1em">
              <Tab width="50%">Login</Tab>
              <Tab width="50%">Signup</Tab>
              <Tab width="50%">Admin</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Login></Login>
              </TabPanel>
              <TabPanel>
                <SignUp></SignUp>
              </TabPanel>
              <TabPanel>
                <AdminLogin></AdminLogin>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Box>
      </Box>
    </>
    // </Container>
  );
};

export default Homepage;
