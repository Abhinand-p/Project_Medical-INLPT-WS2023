import React, { useState, useEffect } from "react";
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
  const [data, setData] = useState<string>("");
  const [prop, setProp] = useState<string>("");

  const [selectedOption1, setSelectedOption1] = useState<string>('');
  const [selectedOption2, setSelectedOption2] = useState<string>('');
  const [selectedOption3, setSelectedOption3] = useState<string>('');
  const [openSearchIndices, setOpenSearchIndices] = useState<[]>([]);

  const handleDropdownChange1 = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption1(event.target.value);
  };

  const handleDropdownChange2 = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption2(event.target.value);
  };
  const handleDropdownChange3 = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption3(event.target.value);
  };

  useEffect(() => {
    console.log("inside useeffect")
    const request = new Request("http://127.0.0.1:8000/getOpenSearchIndices", {
      method: "GET",
    });
    async function getIndicies(this: any){
      try{
        console.log("calling")
        const response = await fetch(request);
        const data = await response.json();
        setOpenSearchIndices(data)
      }
      catch(error){
        console.log(error)
  
      }
    }
    getIndicies()

  }, []); 


  const request = new Request("http://127.0.0.1:8000/get-answer-from-local", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: newMessage,
    }),
  });

  const checkInput = () => {
    if (newMessage.trim() != "") {
      handleSendMessage();
    } else {
      alert("Message can't be empty!");
    }
  };

  async function handleSendMessage() {
    console.log(newMessage);
    setMessages([...messages, { text: newMessage, type: "user" }]);
    setNewMessage("");
    try {
      const response = await fetch(request);
      const data = await response.json();
      console.log(data);

      if (response.status === 200) {
        setMessages((prevMessages: any) => [
          ...prevMessages,
          { text: data, type: "assistant" },
        ]);
      } else {
        console.log("Something went wrong");
      }
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <><Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "50%",
        width: "50%",
        position: "absolute",
        top: "50%",
        left: "40%",
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
                justifyContent: message.type === "user" ? "flex-end" : "flex-start",
              }}
            >
              <ListItemText
                sx={{
                  textAlign: message.type === "user" ? "right" : "left",
                }}
                primary={<Typography
                  variant="body1"
                  sx={{
                    backgroundColor: message.type === "user" ? "lightblue" : "grey",
                    padding: "5px",
                    borderRadius: "10px",
                    display: "inline-block",
                  }}
                >
                  {message.text}
                </Typography>} />
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
          } }
          variant="outlined"
          placeholder="Write a message"
          sx={{
            flexGrow: 1,
            marginRight: 1,
            borderColor: "primary.main",
            borderWidth: 2,
            borderRadius: "5px",
          }}
          inputProps={{ maxLength: MAX_CHARACTERS }} />
        <Typography variant="body2">
          {MAX_CHARACTERS - newMessage.length}/4000
        </Typography>
        <Button onClick={checkInput} variant="contained">
          Send
        </Button>
      </Box>
    </Box>
    <Box sx={{
        display: "flex",
        flexDirection: "column",
        height: "50%",
        width: "20%",
        position: "absolute",
        top: "50%",
        left: "75%",
        transform: "translate(-50%, -50%)",
        border: "1px solid gray",
        borderRadius: "10px",
        marginLeft: "10px"
      }}>
      
      <div className="dropdown">
        <select id="dropdown1" value={selectedOption1} onChange={handleDropdownChange1}>
          <option value="">Retrieval Strategy</option>
          <option value="Dense Retrieval">Dense Retrieval</option>
          <option value="Sarse Retrieval">Sparse Retrieval</option>
          <option value="Hybrid Search">Hybrid Search</option>
        </select>
      </div>

      <div className="dropdown">
        <select id="dropdown2" value={selectedOption2} onChange={handleDropdownChange2}>
        <option value="">Select an Index</option>
        {openSearchIndices.map(item => (
            <option value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      <div className="dropdown">
        <select id="dropdown3" value={selectedOption3} onChange={handleDropdownChange3}>
        <option value="">Select a LLM</option>
        <option value="GPT 3.5 Turbo 0125">GPT 3.5 Turbo 0125</option>
        <option value="LLama-2-7b-chat-hf">LLama-2-7b-chat-hf</option>
        </select>
      </div>


  
      </Box>

      
      </>
  );
};

export default ChatComponent;
