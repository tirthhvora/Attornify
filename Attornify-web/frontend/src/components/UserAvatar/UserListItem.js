import { Avatar, Box, Text } from "@chakra-ui/react";
import React from "react";

const UserListItem = ({ user, handleFunction }) => {
  return (
    <div>
      <Box
        onClick={handleFunction}
        cursor="pointer"
        bg="#E8E8E8"
        _hover={{ background: "#38B2AC", color: "white" }}
        w="100%"
        display="flex"
        alignItems="center"
        color="black"
        px={5}
        py={2}
        mb={2}
        borderRadius="lg"
      >
        <Avatar
          mr={2}
          size="sm"
          cursor="pointer"
          name={user.name}
          src={user.pic}
        ></Avatar>
        <Box>
          <Text>{user.name}</Text>
          <Text fontSize="xs">Email: {user.email}</Text>
        </Box>
      </Box>
    </div>
  );
};

export default UserListItem;
