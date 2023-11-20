import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";

type MessageType = {
  text: string;
  type: "user" | "assistant";
};

const MAX_CHARACTERS = 4000;

const ChatComponent: React.FC = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [newMessage, setNewMessage] = useState<string>("");

  const handleSendMessage = () => {
    setMessages([...messages, { text: newMessage, type: "user" }]);
    setNewMessage("");
    setTimeout(() => {
      setMessages((prevMessages: any) => [
        ...prevMessages,
        { text: "Ja, mache ich", type: "assistant" },
      ]);
    }, 1000);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "50%",
        width: "50%",
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        border: "1px solid gray",
        borderRadius: "10px",
      }}
    >
      <Box sx={{ overflow: "auto", flexGrow: 1 }}>
        <List>
          {messages.map((message: any, index: any) => (
            <ListItem
              key={index}
              sx={{
                justifyContent:
                  message.type === "user" ? "flex-end" : "flex-start",
              }}
            >
              <ListItemText
                sx={{
                  textAlign: message.type === "user" ? "right" : "left",
                }}
                primary={
                  <Typography
                    variant="body1"
                    sx={{
                      backgroundColor:
                        message.type === "user" ? "lightblue" : "grey",
                      padding: "5px",
                      borderRadius: "10px",
                      display: "inline-block",
                    }}
                  >
                    {message.text}
                  </Typography>
                }
              />
            </ListItem>
          ))}
        </List>
      </Box>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          padding: 1,
          borderTop: "1px solid gray",
        }}
      >
        <TextField
          value={newMessage}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
            setNewMessage(e.target.value);
          }}
          variant="outlined"
          placeholder="Write a message"
          sx={{
            flexGrow: 1,
            marginRight: 1,
            borderColor: "primary.main",
            borderWidth: 2,
            borderRadius: "5px",
          }}
          inputProps={{ maxLength: MAX_CHARACTERS }}
        />
        <Typography variant="body2">
          {MAX_CHARACTERS - newMessage.length}/4000
        </Typography>
        <Button onClick={handleSendMessage} variant="contained">
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatComponent;
